import os
import time
import uuid

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.core.management import call_command
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.views.generic import (TemplateView, DetailView, ListView)
from django.core.mail import send_mail

from kxwheels.apps.kx.models import (TireManufacturer,
                       Tire,
                       TireSize,
                       Task,
                       TireReview,
                       TireCustomerMedia,)
from kxwheels.apps.kx.forms import TireSizeSearchForm, StaggeredSearchForm, TireReviewForm, TireCustomerMediaForm
from kxwheels.apps.kx.tasks import import_tires
from kxwheels.apps.vehicle.models import Model


class TireLandingView(TemplateView):
    template_name = "kx/tire/landing.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['tiresize_search_form'] = TireSizeSearchForm()
        return self.render_to_response(context)

class TireManufacturerListView(ListView):
    template_name = "kx/manufacturer_list.html"
    context_object_name = 'manufacturer_list'
    model = TireManufacturer

    def get_queryset(self):
        return TireManufacturer.objects.visible()


class TireListView(ListView):
    model = Tire
    paginate_by = 20
    context_object_name = 'tire_list'
    template_name = "kx/tire/list.html"

    def get_queryset(self):
        self.tire_manufacturer = get_object_or_404(TireManufacturer,
            slug=self.kwargs['slug'])
        return Tire.objects.filter(manufacturer=self.tire_manufacturer)

    def get_context_data(self, **kwargs):
        context = super(TireListView, self).get_context_data(**kwargs)
        context['tire_manufacturer'] = self.tire_manufacturer
        return context


class TireDetailView(DetailView):
    context_object_name = 'tire'
    queryset = Tire.objects.all()
    template_name = "kx/tire/detail.html"

    def get_context_data(self, **kwargs):
        context = super(TireDetailView, self).get_context_data(**kwargs)
        tiresize_pk = self.request.GET.get('s', None)
        if tiresize_pk is not None:
            self.tiresize = get_object_or_404(TireSize, pk=tiresize_pk)
            context['tiresize'] = self.tiresize

        tire = self.get_object()

        print "This is my tire:" + str(tire)

        # Reviews
        reviews = TireReview.approved.filter(reviewee=tire)
        context['reviews'] = reviews

        # Customer media
        customer_media = TireCustomerMedia.active.filter(tire=tire)
        context['customer_media'] = customer_media
        context['auth_and_active_user'] = self.request.user.is_authenticated()
        
        return context


class TireCustomerMediaView(TemplateView):
    template_name = 'kx/customer_media_form.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        tire = get_object_or_404(Tire, pk=kwargs.get('pk'))
        context['tire'] = tire
        form = TireCustomerMediaForm(user=request.user)
        context['form'] = form
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        tire = get_object_or_404(Tire, pk=kwargs.get('pk'))
        context['tire'] = tire
        form = TireCustomerMediaForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            customer_media = form.save(commit=False)
            customer_media.tire = tire
            if request.user.is_authenticated():
                customer_media.user = request.user
            customer_media.save()
            send_mail('Tire Media Review', 'Someone entered a media review for the tire %s.'%tire, 'mailer@kxwheels.com',
    ['info@kxwheels.com'], fail_silently=False)
            return HttpResponseRedirect(reverse('tire_customer_media',
                args=[tire.pk]))

        context['form'] = form
        return self.render_to_response(context)


class TireReviewsView(TemplateView):
    template_name = 'kx/review_form.html'
    rating_fields = ['rating', 'dry_rating', 'noise_rating',
                     'offroad_rating', 'wet_rating', 'comfort_rating', 'snow_rating',
                     'treadwear_rating']

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['rating_fields'] = self.rating_fields
        tire = get_object_or_404(Tire, pk=kwargs.get('pk'))
        context['object'] = tire
        form = TireReviewForm(reviewer=request.user)
        context['form'] = form
        return self.render_to_response(context)


    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['rating_fields'] = self.rating_fields
        tire = get_object_or_404(Tire, pk=kwargs.get('pk'))
        context['object'] = tire
        form = TireReviewForm(request.POST, reviewer=request.user)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewee = tire
            if request.user.is_authenticated() and request.user.is_active:
                review.reviewer = request.user
                review.name = request.user.get_full_name()
                review.ip = request.META.get('HTTP_X_FORWARDED_FOR', "") or request.META.get('REMOTE_ADDR')
            review.save()
            send_mail('Tire Review', 'Someone entered a review for the tire %s.'%tire, 'mailer@kxwheels.com',
    ['info@kxwheels.com'], fail_silently=False)
            return HttpResponseRedirect(reverse('tire_reviews',
                args=[tire.pk]))

        context['form'] = form
        return self.render_to_response(context)


class TireSizeSearchView(TemplateView):
    template_name = 'kx/tire/tiresize_search_form.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        initial = dict(
            prefix=request.GET.get('prefix'),
            treadwidth=request.GET.get('treadwidth'),
            profile=request.GET.get('profile'),
            diameter=request.GET.get('diameter')
        )
        context['form'] = TireSizeSearchForm(initial=initial)
        context['content_type_id'] = ContentType.objects.get_for_model(TireSize).pk

        return self.render_to_response(context)


class TireVehicleSearchView(TemplateView):
    template_name = 'kx/tire/vehicle_search_form.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        vehicle = Model.get_from_cache(request)
        if vehicle is None:
            return HttpResponseRedirect('/')
        context['vehicle'] = vehicle
        return self.render_to_response(context)


class StaggeredSearchView(TemplateView):

    template_name = 'kx/tire/staggered_search_form.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        initial = dict(
            prefix_front=request.GET.get('prefix_front'),
            treadwidth_front=request.GET.get('treadwidth_front'),
            profile_front=request.GET.get('profile_front'),
            diameter_front=request.GET.get('diameter_front'),

            prefix_rear=request.GET.get('prefix_rear'),
            treadwidth_rear=request.GET.get('treadwidth_rear'),
            profile_rear=request.GET.get('profile_rear'),
            diameter_rear=request.GET.get('diameter_rear'),
        )

        form = StaggeredSearchForm(initial=initial)
        context['form'] = form
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = StaggeredSearchForm(request.POST)

        if form.is_valid():
            results = list()

            tiresizes_front = TireSize.objects.filter(
                prefix=form.cleaned_data['prefix_front'],
                treadwidth=form.cleaned_data['treadwidth_front'].value,
                profile=form.cleaned_data['profile_front'].value,
                diameter=form.cleaned_data['diameter_front'].value,
            )

            for tiresize_front in tiresizes_front:
                tiresize_rear = TireSize.objects.filter(
                    tire=tiresize_front.tire,
                    prefix=form.cleaned_data['prefix_rear'],
                    treadwidth=form.cleaned_data['treadwidth_rear'].value,
                    profile=form.cleaned_data['profile_rear'].value,
                    diameter=form.cleaned_data['diameter_rear'].value,
                )

                if tiresize_rear:
                    results.append((tiresize_front, tiresize_rear[0]))

            context['results'] = results

        context['form'] = form

        '''
        # Bypassing haystack search for now
        query = urllib.urlencode(request.POST)
        url = 'http://localhost:8002/search/tire/staggered/?%s' % query
        response = urllib.urlopen(url).read()
        context['results'] = response
        '''
        return self.render_to_response(context)

class TireImportView(TemplateView):
    template_name = 'kx/import.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        tasks = Task.objects.filter(
            session=request.session.session_key,
            is_completed=False
        ).order_by('-created_at')
        context['tasks'] = tasks

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        app = 'tire'
        file = request.FILES.get('file', None)
        if file is None:
            return HttpResponseRedirect(reverse('tire_import'))

        rel = lambda *x: os.path.join(os.path.abspath(
            os.path.dirname(__file__)), *x)

        # Create a backup
        '''
        dumppath = rel('../static/dbdump/')
        if not os.path.exists(dumppath):
            os.makedirs(dumppath)
        dumpout = open('%s/%s.json' % (dumppath, str(int(time.time()))), 'w')
        call_command('dumpdata', app, format='json', stdout=dumpout)
        dumpout.close()
        '''

        new_file = '/tmp/%s' % uuid.uuid4().hex
        with open(new_file, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
            destination.close()

        import_tires(new_file)
        '''
        # Schedule task
        result = import_tires.delay(new_file)

        # Save task
        task, is_created = Task.objects.get_or_create(
            session=request.session.session_key,
            task=result, is_completed=False,
        )
        if is_created:
            task.save()
        '''

        return HttpResponseRedirect(reverse('tire_import'))

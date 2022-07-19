import os
import time
import uuid
import logging
import datetime
from urllib import urlencode
from django.core.files.storage import FileSystemStorage
import csv
import Cookie
from datetime import timedelta
from kxwheels.settings.base import *

from collections import OrderedDict

from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.core.management import call_command
from django.contrib.contenttypes.models import ContentType
from django.views.generic import (TemplateView, DetailView, ListView)
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail

from haystack.query import SQ, SearchQuerySet

from kxwheels.apps.kx.models import WheelManufacturer,FeaturedBrand, Wheel, WheelSize, Task, WheelReview, WheelCustomerMedia
from kxwheels.apps.kx.tasks import import_wheels
from kxwheels.apps.kx.forms import WheelSizeSearchForm, VehicleSearch, WheelReviewForm, WheelCustomerMediaForm
from kxwheels.apps.kx.utils import cut_decimals

from kxwheels.apps.vehicle.models import Model

# Temporary imports
from django.http import HttpResponse

logger = logging.getLogger('project.navdeep')

class WheelLandingView(TemplateView):
    template_name = "kx/wheel/landing.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['wheelsize_search_form'] = WheelSizeSearchForm()
        return self.render_to_response(context)

class WheelManufacturerListView(ListView):
    template_name = "kx/manufacturer_list.html"
    context_object_name = 'manufacturer_list'
    model = WheelManufacturer

    def get_queryset(self):
        return WheelManufacturer.objects.visible()

class WheelFeaturedListView(ListView):
    template_name = "kx/featured_list.html"
    context_object_name = 'featured_list'
    model = FeaturedBrand

    def get_queryset(self):
        return FeaturedBrand.objects.visible()

class MarkedasFeatured(TemplateView):
    template_name = "kx/manufacturer_list.html"
    context_object_name = 'manufacturer_list'
    model = WheelManufacturer,FeaturedBrand

    def post(self, request, *args, **kwargs):
        featured_id = request.POST.get('id', None)
        #  print featured_id
        data=WheelManufacturer.objects.get(id=featured_id)
        feature=FeaturedBrand()
        for field in data.__dict__.keys():
            feature.__dict__[field] = data.__dict__[field]
        feature.save()
        try:
            return JsonResponse({'message':'Feature Added Successfully'})
        except Exception as e:
            return JsonResponse({'message':'Some Error Ocurr,Please try again'})


class WheelListView(ListView):
    model = Wheel
    paginate_by = 25
    context_object_name = 'wheel_list'
    template_name = "kx/wheel/list.html"

    def get_queryset(self):
        self.wheel_manufacturer = get_object_or_404(WheelManufacturer, slug=self.kwargs['slug'])
        return Wheel.objects.filter(manufacturer=self.wheel_manufacturer)

    def get_context_data(self, **kwargs):
        context = super(WheelListView, self).get_context_data(**kwargs)
        context['wheel_manufacturer'] = self.wheel_manufacturer
        return context

class WheelDetailView(DetailView):
    context_object_name = 'wheel'
    queryset = Wheel.objects.all()
    template_name = "kx/wheel/detail.html"

    def get_context_data(self, **kwargs):
        context = super(WheelDetailView, self).get_context_data(**kwargs)
        wheelsize_pk = self.request.GET.get('s', None)
        if wheelsize_pk and wheelsize_pk != 'undefined':
            self.wheelsize = get_object_or_404(WheelSize, pk=wheelsize_pk)
            context['wheelsize'] = self.wheelsize

        wheel = self.get_object()

        # Reviews
        reviews = WheelReview.approved.filter(reviewee=wheel)
        context['reviews'] = reviews

        # Customer media
        customer_media = WheelCustomerMedia.active.filter(wheel=wheel)
        context['customer_media'] = customer_media
        context['auth_and_active_user'] = self.request.user.is_authenticated()

        return context


class ImportWheelCsv(TemplateView):
    value = 0
    template_name = 'kx/wheel/import_wheel.html'
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.GET.get('action') == "get_imported_records":
            if not os.path.isfile(IMPORT_WHEEL + "wheel.log"):
                return JsonResponse({"success": 1, "count": 'ALL'})
            else:
                return JsonResponse({"success": 1, "count": 1})
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.POST.get('action') == 'check_file':
            print '1:check_file'
            if os.path.isfile(IMPORT_WHEEL + "wheel.csv"):
                return JsonResponse({"success": 1})
            else:
                return JsonResponse({"success": 0})

        if request.POST.get('action') == 'terminate':
            print '2:terminate'
            try:
                os.system('rm Home/Documents/djangoprojects/kxwheels/imported_wheels/wheel.csv')
                os.system('rm Home/Documents/djangoprojects/kxwheels/imported_wheels/wheel.log')
            except Exception as e:
                print '________________________________'
                print e
                print '________________________________'
            return JsonResponse({"success": 1})

        if request.POST.get('action') == 'run_script':
            print '3:run_script'
            f_name = request.POST.get('val')
            f_name = IMPORT_WHEEL+f_name
            os.system('python manage.py import_wheels %s >> Home/Documents/djangoprojects/kxwheels/imported_wheels/wheel.log 2>&1 &' % f_name)
            return JsonResponse({"success": 1})
            # print 'After Script'

        ALLOWED_EXTENSTIONS = {"xls", "csv"}
	VALID_COLUMNS = (
            'manufacturer', 'wheel', 'finish', 'diameter', 'wheelwidth', 'boltpattern_1', 'boltpattern_2', 'offset', 'centerbore', 'availability',
            'sku', 'quantity', 'price', 'weight', 'picture_1', 'picture_2', 'picture_3', 'picture_4', 'meta_keywords', 'meta_description',
            'description',
        )
        file = request.FILES.get('file', None)
        print file
        fs = FileSystemStorage(IMPORT_WHEEL)
        if os.path.isfile(IMPORT_WHEEL + "wheel.csv"):
            print 'eerrror'
            context['error'] = "error"
        else:
            import csv
            print 'in elseeee'
            file_name = fs.save("wheel.csv", request.FILES['file'])
            with open(fs.path(file_name), 'rU') as data:
                datadict = {}
                rows = csv.reader(data)
                fieldnames = rows.next()
                if set(VALID_COLUMNS).difference(set(fieldnames)):
                    context['error_columns'] = "wrong"
                    os.remove(IMPORT_WHEEL + 'wheel.csv')
                    return self.render_to_response(context)
            if file is None:
                return HttpResponseRedirect(reverse('csv_import'))
            filename = request.FILES.get('file').name
            ext = filename.split(".")[1]
            if ext not in ALLOWED_EXTENSTIONS:
                context['extension_error'] = "Please upload valid file"
            else:
                context['file_name'] = fs.path(file_name)
                context['yes'] = "importing"
        return self.render_to_response(context)

class ImportImages(TemplateView):
    template_name = 'kx/wheel/import_images.html'

    def get(self, request, *args, **kwargs):

        context = self.get_context_data(**kwargs)
        if request.GET.get('action') == "get_imported_records":
            print datetime.date.today()
            print WheelSize.objects.filter(created_at__date=datetime.date.today()).count()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        brand_name = request.POST.get('brand_name', None)
        if brand_name is None:
            context['error'] = "Please enter brand name"
        else:
            os.system('python manage.py scrap_images %s &' % brand_name)

        return self.render_to_response(context)

class WheelSizeDetailView(DetailView):
    slug_field = 'sku'
    context_object_name = 'wheelsize'
    queryset = WheelSize.objects.all()



class WheelSizeStaggeredDetailView(TemplateView):
    template_name = 'kx/wheel/wheelsize_staggered_detail.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        vehicle = Model.get_from_cache(request)
        front = get_object_or_404(WheelSize, pk=kwargs.get('sku_front'))
        setattr(front, 'recommended_tires', vehicle.get_plus_tire_sizes().filter(diameter=cut_decimals(front.diameter)))


        rear = get_object_or_404(WheelSize, pk=kwargs.get('sku_rear'))
        setattr(rear, 'recommended_tires', vehicle.get_plus_staggered_tire_sizes().filter(rear_diameter=cut_decimals(rear.diameter)))

        context['front'], context['rear'] = front, rear
        return self.render_to_response(context)


class WheelCustomerMediaView(TemplateView):
    template_name = 'kx/customer_media_form.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        wheel = get_object_or_404(Wheel, pk=kwargs.get('pk'))
        context['wheel'] = wheel
        form = WheelCustomerMediaForm(user=request.user)
        context['form'] = form
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        wheel = get_object_or_404(Wheel, pk=kwargs.get('pk'))
        context['wheel'] = wheel
        form = WheelCustomerMediaForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            customer_media = form.save(commit=False)
            customer_media.wheel = wheel
            if request.user.is_authenticated():
                customer_media.user = request.user
            customer_media.save()
            send_mail('Media Review', 'Someone entered a media review for the wheel %s.'%wheel, 'mailer@kxwheels.com',
    ['info@kxwheels.com'], fail_silently=False)
            return HttpResponseRedirect(reverse('wheel_customer_media',
                args=[wheel.pk]))

        context['form'] = form
        return self.render_to_response(context)
    

class WheelReviewsView(TemplateView):
    template_name = 'kx/review_form.html'
    rating_fields = ['rating', ]

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['rating_fields'] = self.rating_fields
        wheel = get_object_or_404(Wheel, pk=kwargs.get('pk'))
        context['object'] = wheel
        form = WheelReviewForm(reviewer=request.user)
        context['form'] = form
        return self.render_to_response(context)


    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['rating_fields'] = self.rating_fields
        wheel = get_object_or_404(Wheel, pk=kwargs.get('pk'))
        context['object'] = wheel
        form = WheelReviewForm(request.POST, reviewer=request.user)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewee = wheel
            if request.user.is_authenticated() and request.user.is_active:
                review.reviewer = request.user
                review.name = request.user.get_full_name()
            review.ip = request.META.get('HTTP_X_FORWARDED_FOR', "") or request.META.get('REMOTE_ADDR')
            print "This is a review: " + repr(review)
            review.save()
            send_mail('Wheel Review', 'Someone entered a review for the wheel %s.'%wheel, 'mailer@kxwheels.com',
    ['info@kxwheels.com'], fail_silently=False)
            return HttpResponseRedirect(reverse('wheel_reviews',
                args=[wheel.pk]))

        context['form'] = form
        return self.render_to_response(context)

        
class WheelSizeSearchView(TemplateView):
    template_name = 'kx/wheel/wheelsize_search_form.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        initial = dict(
            boltpattern=request.GET.get('boltpattern'),
            wheelwidth=request.GET.get('wheelwidth'),
            diameter=request.GET.get('diameter')
        )
        form = WheelSizeSearchForm(initial=initial)
        context['form'] = form
        context['content_type_id'] = ContentType.objects.get_for_model(WheelSize).pk
        return self.render_to_response(context)

class WheelVehicleSearchView(TemplateView):
    template_name = 'kx/wheel/vehicle_search_form.html'

    def get(self, request, *args, **kwargs):
        from django.db.models import Q
        context = self.get_context_data(**kwargs)
        params = request.GET.copy()
        try:
            del(params['page'])
        except KeyError:
            pass
        context['params'] = urlencode(params)
        # We need to have a vehicle in session object to continue
        vehicle = Model.get_from_cache(request)
        if vehicle is None:
            return HttpResponseRedirect('/')
        context['vehicle'] = vehicle

        form = VehicleSearch(request.GET, initial=request.GET)

        # Holds all the filters for wheelsize
        sqs = WheelSize.objects
        
        # Fixed/Required filters: Boltpattern and centerbore
        sqs = sqs.filter(Q(boltpattern_1=vehicle.boltpattern) | Q(boltpattern_2=vehicle.boltpattern))
        
        # Wheel query
        query = Q(sizes__boltpattern_1=vehicle.boltpattern) | Q(sizes__boltpattern_2=vehicle.boltpattern)
        
        # Search Filters from the form
        if form.is_valid():
            manufacturer = form.cleaned_data.get('manufacturer', None)
            if manufacturer is not None:
                query = query & Q(manufacturer=manufacturer)
                sqs = sqs.filter(Q(wheel__manufacturer=manufacturer))

            finish = form.cleaned_data.get('finish', None)
            if finish is not None:
                query = query & Q(sizes__finish__exact=finish)
                sqs = sqs.filter(Q(finish__exact=finish))

            price_from = form.cleaned_data.get('price_from', None) or 0
            price_to = form.cleaned_data.get('price_to', None)

            if price_from and price_to:
                query = query & Q(sizes__price__range=(price_from, price_to))
                sqs = sqs.filter(Q(price__range=(price_from, price_to)))
            if not price_from and price_to:
                query = query & Q(sizes__price__range=(0, price_to))
                sqs = sqs.filter(Q(price__range=(0, price_to)))
                
            diameter = form.cleaned_data.get('diameter', None)
            if diameter:
                query = query & Q(sizes__diameter=diameter)
                sqs = sqs.filter(Q(diameter=diameter))
            #else:
            #    sqs = sqs.filter(SQ(diameter=request.session['vehicle_diameter']))
        context['form'] = form

        split = lambda s: [float(i.strip()) for i in s.split(',')]

        vehicle_front = vehicle.get_front_wheel_size()
        vehicle_rear =  vehicle.get_rear_wheel_size()
        from django.db.models import Q
        if vehicle_front:
            is_vehicle_front = True
            fdr = split(getattr(vehicle_front, 'diameter_range', '0,32'))
            fwr = split(getattr(vehicle_front, 'wheelwidth_range', '0,15'))
            fosr = split(getattr(vehicle_front, 'offset_range', '-200,200'))
            fosr = map(lambda n: int(round(float(n))), fosr)

            if vehicle_rear:
                rdr = split(getattr(vehicle_rear, 'diameter_range', '0,32'))
                rwr = split(getattr(vehicle_rear, 'wheelwidth_range', '0,15'))
                rosr = split(getattr(vehicle_rear, 'offset_range', '-200,200'))
                rosr = map(lambda n: int(round(float(n))), rosr)

                # front and rear
                sqs = sqs.filter(Q(diameter__range=fdr) | Q(diameter__range=rdr))\
                .filter(Q(wheelwidth__range=fwr) | Q(wheelwidth__range=rwr))\
                .filter(Q(offset__range=fosr) | Q(offset__range=rosr))
            else:
            
                sqs = sqs.filter(Q(diameter__range=fdr))\
                .filter(Q(wheelwidth__range=fwr))\
                .filter(Q(offset__range=fosr))

            # Always require a front fitment.
            query = query & (Q(sizes__diameter__range=fdr) &
              Q(sizes__wheelwidth__range=fwr) &
              Q(sizes__offset__range=fosr)
            )
   
        query = query & (Q(manufacturer__in=WheelManufacturer.objects.visible()))
        sqs = sqs.filter(Q(wheel__manufacturer__in=WheelManufacturer.objects.visible()))

        wheels = Wheel.objects.filter(query).distinct().order_by('manufacturer__name')

        paginator = Paginator(wheels, 24)
        page = request.GET.get('page', 1)
        try:
            wheels = paginator.page(page)
        except PageNotAnInteger:
            wheels = paginator.page(1)
        except EmptyPage:
            wheels = paginator.page(paginator.num_pages)
        
        try:
          size_query = Q(wheel = wheels.object_list[0])
          for wheel in wheels.object_list[1:]:
              size_query = size_query | Q(wheel = wheel)
          wheelsizes = sqs.filter(size_query)
        except IndexError:
          wheelsizes = []
        
        results = {}
        wheelsizes = [ws for ws in wheelsizes if ws.wheel in wheels.object_list]
        
        # Populate results dict initially
        for ws in wheelsizes:
            results[ws.wheel] = {
                'wheel': ws.wheel,
                'wheel_slug': ws.wheel.slug,
                'manufacturer': ws.wheel.manufacturer,
                'manufacturer_slug': ws.wheel.manufacturer.slug,
                'finish': ws.finish,
                'thumbnail': ws.get_thumbnail_med(),
                'sizes': [],
            }
        
        # Assign wheelsizes to appropriate wheels
        for ws in wheelsizes:

            # Front wheel range
            if vehicle_front:
                if ((fdr[0] <= float(ws.diameter) <= fdr[1]) and
                    (fwr[0] <= ws.wheelwidth <= fwr[1]) and
                    (fosr[0] <= ws.offset <= fosr[1])):
                    setattr(ws, 'front_recommended_tires',
                        vehicle.get_plus_tire_sizes().filter(
                            diameter=cut_decimals(ws.diameter)))

            # Rear wheel range
            if vehicle_rear:
                if ((rdr[0] <= float(ws.diameter) <= rdr[1]) and
                    (rwr[0] <= ws.wheelwidth <= rwr[1]) and
                    (rosr[0] <= ws.offset <= rosr[1])):
                    setattr(ws, 'rear_recommended_tires',
                        vehicle.get_plus_staggered_tire_sizes().filter(
                            rear_diameter=cut_decimals(ws.diameter)))

            if ws.wheel in results:
                results[ws.wheel]['sizes'].append(ws)
            else:
                results[ws.wheel]['sizes'] = [ws]

        # Assign wheelsizes to appropriate diameters
        for key, val in results.items():
            d = dict(((i.diameter, []) for i in val['sizes']))
            for ws in val['sizes']:
                if ws.diameter in d.keys():
                    d[ws.diameter].append(ws)
                else:
                    d[ws.diameter] = [ws]
            results[key]['sizes'] = OrderedDict(sorted(d.items(), key=lambda x: x[0]))

        # convert dict to list
        results_list = []
        for wheel, items in results.items():
            results_list.append(items)

        results_list.sort(key=lambda x: x['manufacturer'].name)
        
        context['wheelsizes'] = results_list
        context['wheels'] = wheels
        context['content_type_id'] = ContentType.objects.get_for_model(WheelSize).pk
        return self.render_to_response(context)

class WheelImportView(TemplateView):
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
        app = 'wheel'
        file = request.FILES.get('file', None)
        if file is None:
            return HttpResponseRedirect(reverse('wheel_import'))

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

        # Schedule task
#result = import_wheels.delay(new_file)
        errors = import_wheels(new_file)
        context['errors'] = errors

        '''
        # Save task
        task, is_created = Task.objects.get_or_create(
            session=request.session.session_key,
            task=result, is_completed=False,
        )
        if is_created:
            task.save()
        '''
        return self.render_to_response(context)

def recommened_tires_json(request):
    vehicle_pk = request.GET.get('v_pk', None)
    front_wheelsize_pk = request.GET.get('f_ws_pk', None)
    rear_wheelsize_pk = request.GET.get('r_ws_pk', None)


    try:
        vehicle = Model.objects.get(pk=vehicle_pk)
    except Vehicle.DoesNotExist:
        pass

    try:
        front_wheelsize = WheelSize.objects.get(pk=front_wheelsize_pk)
    except WheelSize.DoesNotExist:
        pass

    try:
        rear_wheelsize = WheelSize.objects.get(pk=rear_wheelsize_pk)
    except WheelSize.DoesNotExist:
        pass

    plus_staggered_tiresizes = vehicle.get_plus_staggered_tire_sizes().filter(
        front_diameter=front_wheelsize.diameter,
        rear_diameter=rear_wheelsize.diameter,
    )

    result = serializers.serialize('json', plus_staggered_tiresizes,)
    return HttpResponse(result, content_type="application/json")



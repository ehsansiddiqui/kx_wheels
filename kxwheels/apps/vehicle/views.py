import re
import os
#import cjson
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import (TemplateView, DetailView, ListView)
from kxwheels.apps.vehicle.forms import ModelSearchForm
from kxwheels.apps.vehicle.models import (TreadWidth, Profile, Diameter, Manufacturer, Model)
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse

class ManufacturerList(ListView):

    model = Manufacturer

class ModelList(ListView):

    def get_queryset(self):
        self.manufacturer = get_object_or_404(Manufacturer, slug=self.kwargs['manufacturer'])
        return Model.objects.filter(manufacturer=self.manufacturer)
        
    def get_context_data(self, **kwargs):
        context = super(ModelList, self).get_context_data(**kwargs)
        context['manufacturer'] = self.manufacturer
        return context

class ModelDetail(DetailView):
    
    model = Model

    # def get_object(self):
    #     object = super(ModelDetail, self).get_object()
    #     self.request.session['vehicle']=object
    #     return object

class ModelSearchView(TemplateView):
    template_name = 'vehicle/model_search_form.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = ModelSearchForm()
        context['form'] = form
        return self.render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return_path = self.request.POST.get('return_path', '')
        form = ModelSearchForm(request.POST)
        if form.is_valid():
            try:
                model = Model.objects.filter(
                    year=form.cleaned_data['year'],
                    name=form.cleaned_data['model']
                )[0]

                cache.set(Model.get_cache_key(request), model)
            except IndexError:
                pass
            else:
                #request.session['vehicle_diameter'] = form.cleaned_data['diameter']
                if return_path:
                    return HttpResponseRedirect(return_path)
                else:
                    return HttpResponse("OK")
        return self.render_to_response(context)


class VehicleImport(TemplateView):
    template_name = 'vehicle/vehicle_import.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        # form = ModelSearchForm()
        # context['form'] = form
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        ALLOWED_EXTENSTIONS = {"xls", "csv"}
        file = request.FILES.get('file', None)
        if file is None:
            return HttpResponseRedirect(reverse('vehicle_import'))
        filename = request.FILES.get('file').name
        ext = filename.split(".")[1]
        if ext not in ALLOWED_EXTENSTIONS:
            context['extension_error'] = "Please upload valid file"
        else:
            os.system('python manage.py import_vehicles %s &' % file)

        return self.render_to_response(context)


def json_response(response):
    return HttpResponse(cjson.encode(response), content_type="application/json")

def treadwidths(request):
    tws = TreadWidth.objects.all().order_by('sort_order')
    result = []
    for tw in tws:
        result.append({'id': tw.id, 'value': tw.value})
    return json_response(result)

def profiles(request):
    ps = Profile.objects.all().order_by('sort_order')
    result = []
    for p in ps:
        result.append({'id': p.id, 'value': p.value})
    return json_response(result)

def diameters(request):
    ds = Diameter.objects.all().order_by('sort_order')
    result = []
    for d in ds:
        result.append({'id': d.id, 'value': d.value})
    return json_response(result)
    
def manufacturers(request):
    ms = Manufacturer.objects.filter(is_active=1)
    result = []
    for m in ms:
        result.append({'id': m.id, 'name': m.name, 'slug': m.slug})
    return json_response(result)

def manufacturer(request, manufacturer):
    manufacturer = Manufacturer.objects.get(slug=manufacturer)
    result = []
    for model in manufacturer.models.all():
        result.append({'id': model.id, 'name': model.name, 'slug': model.slug})
    return json_response(result)

def model(request, manufacturer, model):
    try:
        model = Model.objects.get(slug=model)
    except Model.DoesNotExist:
        result = {}
    else:
        result = {
            'id': model.id,
            'name': model.name,
            'slug': model.slug,
        }

        oe_tiresizes = list(model.oe_tiresizes.all().values('treadwidth', 
            'profile', 'diameter'))
        front_tiresizes = list(model.front_tiresizes.all().values('treadwidth', 
            'profile', 'diameter'))
        rear_tiresizes = list(model.rear_tiresizes.all().values('treadwidth', 
            'profile', 'diameter'))

        if oe_tiresizes:
            result['oe_tiresizes'] = oe_tiresizes
        if front_tiresizes:
            result['front_tiresizes'] = front_tiresizes
        if rear_tiresizes:
            result['rear_tiresizes'] = rear_tiresizes
        
    return json_response(result)

def search(request):
    manufacturer = re.sub(r'[^A-Za-z0-9-]', '', request.GET.get('manufacturer'))
    year = int(re.sub(r'[^\d+]', '', request.GET.get('year')))
    
    models = Model.objects.filter(manufacturer=Manufacturer.objects.get(slug=manufacturer), year=year)
    results = []
    for model in models:
        results.append({
            'id': model.id,
            'name': model.name,
            'slug': model.slug,
        })

    return json_response(results)

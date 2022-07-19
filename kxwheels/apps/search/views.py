import json
from haystack.views import SearchView
from django.views.generic import TemplateView
from haystack.query import SearchQuerySet
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render

from django.db import connection, transaction

from django.views.generic import (TemplateView, DetailView, ListView)

from django.db.models import Q

from django.core.urlresolvers import reverse

from kxwheels.apps.kx.models import TireSize, WheelSize, TireManufacturer, WheelManufacturer, Wheel, WheelPicture
from kxwheels.apps.kx.models.wheel import WheelSliderImages, WheelBrandImagesThumbnail
from kxwheels.apps.kx.models.tire import TireBrandImagesThumbnail
from kxwheels.apps.shop.templatetags.shop_filters import currency
from kxwheels.apps.search.decorators import csrf_token_required, api_access_required

class WheelSizeSearchView(SearchView):
    results_per_page = 36

    def normalize(self, object_list):
        results = []
        for o in object_list:
            wheelsize = {}

            # Populate wheelsize
            for key, value in o.get_stored_fields().items():
                if type(value) is unicode: value = value.encode('ascii','ignore')
                wheelsize[key] = value if str(value) else ''
            # Price
            wheelsize_object = WheelSize.objects.get(pk=o.pk)
            wheelsize['price'] = currency(wheelsize_object.get_price(self.request.user))

            wheelsize['permalink'] = reverse('wheel_wheelsize_detail', args=[o.manufacturer_slug, o.wheel_slug, o.pk])
            del(wheelsize['text'])

            results.append(wheelsize)
        return results

    @csrf_token_required
    @api_access_required
    def create_response(self):
        """
        Generates the actual HttpResponse to send back to the user.
        """
        slug_dict_list = WheelManufacturer.objects.visible().values('slug').distinct()
        slugs = []
        for sd in slug_dict_list:
            slugs.append(sd['slug'])
        self.results = self.results.filter(manufacturer__in=slugs)
        self.results = list(self.results)
        self.results.sort(key=lambda x: x.manufacturer)
        (paginator, page) = self.build_page()
        
        context = {
            'query': self.query,
            'form': self.form,
            'page': page,
            'paginator': paginator,
            'suggestion': None,
        }


        context.update(self.extra_context())
        results = self.normalize(page.object_list)
        info = {
            'count': paginator.count,
            'page': page.number,
            'total_pages': paginator.num_pages, 
        }
        _json = json.dumps({'info': info, 'results': results})
        return HttpResponse(_json, content_type="application/json")



class VehicleSearchView(WheelSizeSearchView):
    results_per_page = 10000

class ModelSearchView(SearchView):
    results_per_page = 100
    
    def normalize(self, object_list):
        results = []
        for o in object_list:
            results.append({
                'pk': o.pk,
                'manufacturer': o.manufacturer,
                'manufacturer_slug': o.manufacturer_slug,
                'name': o.name,
                'slug': o.slug,
                'year': o.year,
            })
        return results

    @csrf_token_required
    @api_access_required
    def create_response(self):
        (paginator, page) = self.build_page()
       
        context = {
            'query': self.query,
            'form': self.form,
            'page': page,
            'paginator': paginator,
            'suggestion': None,
        }
        context.update(self.extra_context())
        results = self.normalize(page.object_list)
        info = {
            'count': paginator.count,
            'page': page.number,
            'total_pages': paginator.num_pages, 
        }
        _json = json.dumps({'info': info, 'results': results})
        return HttpResponse(_json, "application/json")
    
class TireSizeSearchView(SearchView):
    results_per_page = 150
    
    def normalize(self, object_list):
        results = []
        for o in object_list:
            tiresize = {}
                      
            # Populate tiresize
            for key, value in sorted(o.get_stored_fields().items()):
                tiresize[key] = value if value else ''

            # Add pk
            tiresize['pk'] = o.pk

            # Price
            tiresize_object = TireSize.objects.get(pk=o.pk)
            tiresize['price'] = currency(tiresize_object.get_price(self.request.user))
            
            # Permalink
            tiresize['permalink'] = reverse('tire_tiresize_detail', args=[o.manufacturer_slug, o.tire_slug, o.pk])

            # Remove text key
            del(tiresize['text'])
            
            results.append(tiresize)
            
            
        return results

    @csrf_token_required
    @api_access_required
    def create_response(self):
        slug_dict_list = TireManufacturer.objects.visible().values('slug').distinct()
        slugs = []
        for sd in slug_dict_list:
            slugs.append(sd['slug'])
        self.results = self.results.filter(manufacturer__in=slugs)
        (paginator, page) = self.build_page()
       
        context = {
            'query': self.query,
            'form': self.form,
            'page': page,
            'paginator': paginator,
            'suggestion': None,
        }
        
        context.update(self.extra_context())
        results = self.normalize(page.object_list)
        info = {
            'count': paginator.count,
            'page': page.number,
            'total_pages': paginator.num_pages, 
        }
        _json = json.dumps({'info': info, 'results': results})
        return HttpResponse(_json, "application/json")

class StaggeredSearchView(SearchView):
    results_per_page = 1000

    def normalize(self, object_list):
        results = []
        for o in object_list:
            tiresize = {}

            # Populate tiresize
            for key, value in o.get_stored_fields().items():
                tiresize[key] = value if value else ''

            # Remove text key
            del(tiresize['text'])

            results.append(tiresize)
        return results

    @csrf_token_required
    @api_access_required
    def create_response(self):
        (paginator, page) = self.build_page()

        context = {
            'query': self.query,
            'form': self.form,
            'page': page,
            'paginator': paginator,
            'suggestion': None,
        }

        context.update(self.extra_context())
        results = self.normalize(page.object_list)
        info = {
            'count': paginator.count,
            'page': page.number,
            'total_pages': paginator.num_pages,
        }
        _json = json.dumps({'info': info, 'results': results})
        return HttpResponse(_json, "application/json")


# /z.a.h/e.e.r/ sSearch product, wheel, name, size     /c.o/d.e/  #

class SearchData(TemplateView):
    def set_list_values(self, query, rows_afected):
        row = query.fetchone()
        rows_affected = rows_afected
        list_range = rows_affected * 9
        data_list = [0 for x in range(list_range)]
        i = 0
        while row is not None:
            data_list[i] = row[0]
            data_list[i+1] = row[1]
            data_list[i+2] = row[2]
            data_list[i+3] = row[3]
            data_list[i+4] = row[4]
            data_list[i+5] = row[5]
            data_list[i+6] = row[6]
            data_list[i+7] = row[7]
            data_list[i+8] = int(row[8])
            i += 9
            row = query.fetchone()
            if i == 10 * 9:
                row = None
        return data_list,list_range

    def post(self, request, **kwargs):
        search_data = request.POST
        search_value = search_data['val']
        if ' ' in search_value:
            search_value1 = search_data['val'].split(' ')
            query_value = "'%" + search_value1[0] + "_" + search_value1[1] + "%'"
        else:
            query_value = "'%" +search_value+ "%'"
            print search_value
        cursor = connection.cursor()
        query = "SELECT DISTINCT kx_wheel.id, kx_wheel.name as wheel_name, kx_wheelpicturethumbnail.path AS wheel_pic, kx_wheel.slug as slug, kx_wheelmanufacturer.name, kx_wheelbrandimagesthumbnail.path, kx_wheelmanufacturer.slug, kx_wheelpicture.picture, kx_wheelsize.price FROM kx_wheel INNER JOIN kx_wheelmanufacturer ON kx_wheel.manufacturer_id = kx_wheelmanufacturer.id INNER JOIN kx_wheelsize ON kx_wheel.id = kx_wheelsize.wheel_id INNER JOIN kx_wheelpicture ON kx_wheel.id = kx_wheelpicture.wheel_id INNER JOIN kx_wheelpicturethumbnail ON kx_wheelpicture.id = kx_wheelpicturethumbnail.wheelpicture_id AND kx_wheelpicturethumbnail.size ='med' INNER JOIN kx_wheelbrandimagesthumbnail ON kx_wheelbrandimagesthumbnail.brand_name = kx_wheelmanufacturer.name where cast(kx_wheel.name AS TEXT) ILIKE %s OR cast(kx_wheelsize.diameter AS TEXT) ILIKE %s OR cast(kx_wheelmanufacturer.name AS TEXT) ILIKE %s OR  cast(kx_wheelsize.sku AS TEXT) ILIKE %s LIMIT 10; " % (
            query_value, query_value, query_value, query_value)
        queryy = "SELECT DISTINCT kx_tire.id, kx_tire.name as tire_name, kx_tirepicturethumbnail.path AS tire_pic, kx_tire.slug as slug, kx_tiremanufacturer.name,  kx_tirebrandimagesthumbnail.path, kx_tiremanufacturer.slug, kx_tirepicture.picture, kx_tiresize.price FROM kx_tire INNER JOIN kx_tiremanufacturer ON kx_tire.manufacturer_id = kx_tiremanufacturer.id INNER JOIN kx_tiresize ON kx_tire.id = kx_tiresize.tire_id INNER JOIN kx_tirepicture ON kx_tire.id = kx_tirepicture.tire_id INNER JOIN kx_tirepicturethumbnail ON kx_tirepicture.id = kx_tirepicturethumbnail.tirepicture_id AND kx_tirepicturethumbnail.size ='med' INNER JOIN kx_tirebrandimagesthumbnail ON kx_tirebrandimagesthumbnail.brand_name = kx_tiremanufacturer.name where cast(kx_tire.name AS TEXT) ILIKE %s OR cast(kx_tiresize.diameter AS TEXT) ILIKE %s OR cast(kx_tiremanufacturer.name AS TEXT) ILIKE %s OR  cast(kx_tiresize.sku AS TEXT) ILIKE %s LIMIT 10; " % (
            query_value, query_value, query_value, query_value)
        cursor.execute(query)
        rows_affectedd = cursor.rowcount

        if rows_affectedd:
            data_list1,list_range1 = self.set_list_values(cursor,rows_affectedd)
        cursor.execute(queryy)
        rows_affected = cursor.rowcount

        if rows_affected:
            data_list2, list_range2 = self.set_list_values(cursor, rows_affected)
        if rows_affectedd > 0 and rows_affected> 0:
            list_range = list_range1 + list_range2
            data_list = [0 for x in range(list_range)]
            data_list = data_list1 + data_list2

        elif rows_affectedd > 0:
            data_list = data_list1
        elif rows_affected > 0:
            data_list = data_list2
        else:
            data_list = {"msg": "No record Found", "status": "Fail"}
        cursor.close()

        return HttpResponse(json.dumps(data_list), content_type='Application/json')


class ImageSliders(ListView):
    template_name = 'base_index.html'
    context_object_name = 'manufacturer_list'
    model = WheelSliderImages

    def get_queryset(self):
        images = WheelSliderImages.objects.values('image')
        return images

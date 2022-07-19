from django.conf.urls import include, url
from kxwheels.apps.vehicle.views import *
vehicle_model_search = ModelSearchView.as_view()
vehicle_import = VehicleImport.as_view()

urlpatterns = [
    url(r'^treadwidths/$', treadwidths, name="vehicle_treadwidths"),
    url(r'^profiles/$', profiles, name="vehicle_profiles"),
    url(r'^diameters/$', diameters, name="vehicle_diameters"),
    url(r'^model_browse/(?P<manufacturer>.*)/(?P<slug>.*)/$', ModelDetail.as_view(), name="vehicle_model_detail"),
    url(r'^model_browse/(?P<manufacturer>.*)/$', ModelList.as_view(), name="vehicle_model_browse"),
    url(r'^model_browse/$', ManufacturerList.as_view(), name="vehicle_manufacturer_list"),
    url(r'^model_search/$', vehicle_model_search, name="vehicle_model_search"),
    url(r'^vehicle_import/$', vehicle_import, name="vehicle_import"),
    url(r'^(?P<manufacturer>.*)/(?P<model>.*)/$', model, name="vehicle_model"),
    url(r'^(?P<manufacturer>.*)/$', manufacturer, name="vehicle_manufacturer"),
    url(r'^$', manufacturers, name="vehicle_manufacturers"),
]

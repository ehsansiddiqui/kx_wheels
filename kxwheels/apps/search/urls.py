from django.conf.urls import include, url
from kxwheels.apps.search.views import *
from kxwheels.apps.search import views
from kxwheels.apps.kx.forms import WheelSizeSearchForm, TireSizeSearchForm, StaggeredSearchForm
from kxwheels.apps.vehicle.forms import ModelSearchForm

urlpatterns = [
    url(r'^wheel/wheelsize/$', WheelSizeSearchView(form_class=WheelSizeSearchForm), name='search_wheel_wheelsize'),
    url(r'^wheel/vehicle/$', VehicleSearchView(form_class=WheelSizeSearchForm), name='search_wheel_vehicle'),

    url(r'^tire/tiresize/$', TireSizeSearchView(form_class=TireSizeSearchForm), name='search_tire_tiresize'),
    url(r'^tire/staggered/$', StaggeredSearchView(form_class=StaggeredSearchForm), name='search_tire_staggered'),

    url(r'^vehicle/model/$', ModelSearchView(form_class=ModelSearchForm), name='search_vehicle_model'),
    url(r'^search/$', SearchData.as_view(), name='search_data'),
]

from django.conf.urls import include, url
from django.views.generic import TemplateView
from kxwheels.apps.account.decorators import require_superuser
from kxwheels.apps.kx.views.tire import *
from kxwheels.apps.kx.views.wheel import *
from kxwheels.apps.kx.views.accessories import *

tire_landing = TireLandingView.as_view()
tire_manufacturer_list = TireManufacturerListView.as_view()
tire_tire_list = TireListView.as_view()
tire_tire_detail = TireDetailView.as_view()
tire_tiresize_search = TireSizeSearchView.as_view()
tire_vehicle_search = TireVehicleSearchView.as_view()
tire_staggered_search = StaggeredSearchView.as_view()
tire_import = require_superuser(TireImportView.as_view())
tire_customer_media = TireCustomerMediaView.as_view()
tire_reviews = TireReviewsView.as_view()
tire_tire_calculator = TemplateView.as_view(template_name="kx/tire/calculator.html")


wheel_landing = WheelLandingView.as_view()
wheel_manufacturer_list = WheelManufacturerListView.as_view()
wheel_featured_list = WheelFeaturedListView.as_view()
marked_as_featured = MarkedasFeatured.as_view()

wheel_wheel_list = WheelListView.as_view()
wheel_wheel_detail = WheelDetailView.as_view()
wheel_wheelsize_detail = WheelSizeDetailView.as_view()
wheel_wheelsize_staggered_detail = WheelSizeStaggeredDetailView.as_view()
wheel_wheelsize_search = WheelSizeSearchView.as_view()
wheel_vehicle_search = WheelVehicleSearchView.as_view()
wheel_import = require_superuser(WheelImportView.as_view())
wheel_customer_media = WheelCustomerMediaView.as_view()
wheel_reviews = WheelReviewsView.as_view()
import_images = ImportImages.as_view()
wheel_backspace_calculator = TemplateView.as_view(template_name="kx/wheel/backspace_calculator.html")
csv_import = require_superuser(ImportWheelCsv.as_view())
accessories = KxAccessories.as_view()
accessories_list = KxAccessoriesListView.as_view()
accessories_detail = KxAccessoriesDetailView.as_view()



urlpatterns = [
    url(r'^contact-us/$', TemplateView.as_view(template_name='contact.html'), name="contact"),
    url(r'^tire/$', tire_landing, name='tire_landing'),
    url(r'^tire/calculator/', tire_tire_calculator, name="tire_tire_calculator"),
    url(r'^tire/import/', tire_import, name="tire_import"),
    url(r'^tire/customer_media/(?P<pk>[\d]+)/$', tire_customer_media, name="tire_customer_media"),
    url(r'^tire/reviews/(?P<pk>[\d]+)/$', tire_reviews, name="tire_reviews"),
    url(r'^tire/tiresize_search/', tire_tiresize_search, name="tire_tiresize_search"),
    url(r'^tire/vehicle_search/', tire_vehicle_search, name="tire_vehicle_search"),
    url(r'^tire/staggered_search/', tire_staggered_search, name="tire_staggered_search"),

    url(r'^tire/brands/$', tire_manufacturer_list, name='tire_manufacturer_list'),
    url(r'^tire/(?P<manufacturer>[\d\w-]+)/(?P<slug>[\w-]+)/$', tire_tire_detail, name="tire_tire_detail"),
    url(r'^tire/(?P<manufacturer>[\d\w-]+)/(?P<slug>[\w-]+)/\?s=(?P<pk>[\w-]+)$', tire_tire_detail, name="tire_tiresize_detail"),
    url(r'^tire/(?P<slug>[\w-]+)/$', tire_tire_list, name='tire_tire_list'),
]



urlpatterns += [
    url(r'^wheel/$', wheel_landing, name='wheel_landing'),
    url(r'^wheel/backspace_calculator/$', wheel_backspace_calculator, name="wheel_backspace_calculator"),
    url(r'^wheel/import/$', wheel_import, name="wheel_import"),
    url(r'^wheel/customer_media/(?P<pk>[\d]+)/$', wheel_customer_media, name="wheel_customer_media"),
    url(r'^wheel/reviews/(?P<pk>[\d]+)/$', wheel_reviews, name="wheel_reviews"),
    url(r'^wheel/wheelsize_search/', wheel_wheelsize_search, name="wheel_wheelsize_search"),
    url(r'^wheel/vehicle_search/', wheel_vehicle_search, name="wheel_vehicle_search"),
    url(r'^wheel/rec_tires/$', recommened_tires_json, name="wheel_rec_tires"),

    url(r'^wheel/brands/$', wheel_manufacturer_list, name='wheel_manufacturer_list'),
    url(r'^wheel/featured_brands/$', wheel_featured_list, name='wheel_featured_list'),
    url(r'^wheel/marked_as_featured/$', marked_as_featured, name='marked_as_featured'),
    url(r'^wheel/(?P<manufacturer>[\d\w-]+)/(?P<slug>[\w-]+)/$', wheel_wheel_detail, name="wheel_wheel_detail"),

    url(r'^wheel/(?P<manufacturer>[\d\w-]+)/(?P<wheel_slug>[\w-]+)/\?s=(?P<pk>[\w-]+)$',
        wheel_wheel_detail, name="wheel_wheelsize_detail"),

    url(r'^wheel/(?P<manufacturer>[\d\w-]+)/(?P<wheel_slug>[\w-]+)/(?P<sku_front>[\w\d-]+)/(?P<sku_rear>[\w\d-]+)/$',
        wheel_wheelsize_staggered_detail, name="wheel_wheelsize_staggered_detail"),

    url(r'^wheel/(?P<slug>[\w-]+)/$', wheel_wheel_list, name='wheel_wheel_list'),
    url(r'^import/images/$', import_images, name='import_images'),
    url(r'^import/wheel/$', csv_import, name='csv_import'),
    url(r'^accessories/$', accessories, name='accessories'),
    url(r'^accessories/(?P<slug>[\w-]+)/$', accessories_list, name='accessories_list'),
    url(r'^accessories/(?P<accessories>[\d\w-]+)/(?P<slug>[\w-]+)/$', accessories_detail, name="accessories_detail"),
    # url(r'^import/wheel/(?P<action>[\w-]+)/$', csv_import, name='csv_import'),
    
]

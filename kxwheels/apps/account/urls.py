from django.conf.urls import url
from kxwheels.apps.account.views import LoginView
from registration.backends.model_activation import urls as model_urls

from kxwheels.apps.account.forms import RegistrationFormNoUserName
from kxwheels.apps.account.views import *

register = RegistrationView.as_view()
login_user = LoginView.as_view()

auth_account = AccountView.as_view()
auth_profile_detail = ProfileDetailView.as_view()
auth_profile_list = ProfileListView.as_view()
auth_profile_create = ProfileCreateView.as_view()
auth_profile_update = ProfileUpdateView.as_view()
auth_profile_delete = ProfileDeleteView.as_view()
auth_order_history = OrderHistoryView.as_view()

auth_order_history_logout = OrderHistoryLogoutView.as_view()

auth_dealer_create = DealerCreateView.as_view()
auth_dealer_create_download = DealerCreateDownloadView.as_view()
auth_dealer_create_thanks = DealerCreateThanksView.as_view()

dealer_manufacturer_discounts = DealerManufacturerDiscountsView.as_view()
dealer_orders = DealerOrderListView.as_view()

urlpatterns = [
    url(r'^$', auth_account, name="auth_account"),
    url(r'^markup/$', dealer_manufacturer_discounts, name="dealer_manufacturer_discounts"),
    url(r'^orders/$', dealer_orders, name="dealer_orders"),
    url(r'^profile/$', auth_profile_list, name="auth_profile_list"),
    url(r'^profile/create/(?P<slug>(shipping|billing))/$', auth_profile_create, name="auth_profile_create"),
    url(r'^profile/update/(?P<slug>(shipping|billing))/$', auth_profile_update, name="auth_profile_update"),
    url(r'^profile/delete/(?P<slug>(shipping|billing))/$', auth_profile_delete, name="auth_profile_delete"),
    url(r'^profile/(?P<slug>[-\w]+)/$', auth_profile_detail, name='auth_profile_detail'),

    url(r'^order_history/$', auth_order_history, name='auth_order_history'),
    url(r'^order_history_lgout/$', auth_order_history_logout, name='auth_order_history_logout'),

    url(r'^dealer/create/$', auth_dealer_create, name="auth_dealer_create"),
    url(r'^dealer/download_excel/$', auth_dealer_create_download, name="auth_dealer_download"),
    url(r'^dealer/create/thanks/$', auth_dealer_create_thanks, name="auth_dealer_create_thanks"),


    url(r'^login/$', login_user, name='login_user'),
    url(r'^register/$', register, name='registration_register'),
]

urlpatterns += model_urls.urlpatterns
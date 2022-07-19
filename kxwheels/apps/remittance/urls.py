from django.conf.urls import include, url
from kxwheels.apps.remittance.views import *

remittance_payment_cancel = PaymentCancelView.as_view()
remittance_payment_process = PaymentProcessView.as_view()
remittance_paypal_process = PaypalProcessView.as_view()
remittance_payment_success = PaymentSuccessView.as_view()
remittance_payment_failure = PaymentFailureView.as_view()
remittance_purchase_detail = PurchaseView.as_view()

urlpatterns = [
    url(r'^success/$', remittance_payment_success, name='remittance_payment_success'),
    url(r'^failure/$', remittance_payment_failure, name='remittance_payment_failure'),
    url(r'^process/$', remittance_payment_process, name='remittance_payment_process'),
    url(r'^paypal-process/$', remittance_paypal_process, name='remittance_paypal_process'),
    url(r'^cancel/$', remittance_payment_cancel, name='remittance_payment_cancel'),
    #url(r'^(?P<cache_key>[a-zA-Z0-9]+)/$', remittance_payment_process, name='remittance_payment_process'),
    url(r'^(?P<slug>[a-zA-Z0-9]+)/$', remittance_purchase_detail, name='remittance_purchase_detail'),
]

'''
# Module specific urls
payment_module = get_module()
urlpatterns += patterns('',
    (r'^%s/' % getattr(payment_module, 'settings')['ID'], include('%s.urls' % payment_module.__name__)),
)
'''

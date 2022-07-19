import django.dispatch

order_received = django.dispatch.Signal()
product_save = django.dispatch.Signal()
cart_received_shipping_information = django.dispatch.Signal()

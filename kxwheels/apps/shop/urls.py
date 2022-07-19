from django.conf.urls import include, url
from django.views.decorators.cache import never_cache
from kxwheels.apps.shop.views import (cart, cartitem, order, product, payment)

# Cart
short_summary = cart.ShortSummaryView.as_view()

# CartItem
add_to_cart = cartitem.AddToCartView.as_view()

urlpatterns = [
    url(r'^cart/$', never_cache(cart.read), name="shop_cart"),
    url(r'^cart/success/', never_cache(cart.success), name="shop_success"),
    url(r'^cart/card/', never_cache(cart.card_success), name="shop_card"),
    url(r'^cart/create/$', never_cache(cart.create), name="shop_cart_create"),
    url(r'^cart/delete/$', never_cache(cart.delete), name="shop_cart_delete"),
    url(r'^cart/summary/$', never_cache(cart.summary), name="shop_cart_summary"),
    url(r'^cart/email_value/', never_cache(cart.email_details), name="shop_cart_summary_email"),
    url(r'^cart/short_summary/$', never_cache(short_summary), name="shop_cart_short_summary"),
    url(r'^cart/list/$', never_cache(cart.accessories_view), name='accessories_list_model'),
]

# Cart items
urlpatterns += [
    url(r'^cart/item/create/$', add_to_cart, name="shop_cartitem_create"),
    # url(r'^cart/item/create/$', cartitem.create, name="shop_cartitem_create"),
    url(r'^cart/item/update/$', cartitem.update, name="shop_cartitem_update"),
    url(r'^cart/item/delete/$', cartitem.delete, name="shop_cartitem_delete"),
]

# Order
urlpatterns += [
    url(r'^order/$', never_cache(order.list), name="shop_order_list"),
    url(r'^order/update$', never_cache(order.update), name="shop_order_update"),
    url(r'^order/(?P<object_id>[\d]+)/$', order.read,  name="shop_order_read"),
    url(r'^order/create/$', never_cache(order.create), name="shop_order_create"),
    url(r'^order/delete/$', never_cache(order.delete), name="shop_order_delete"),
    url(r'^product/(?P<content_type_id>[\d]+)/$',
        never_cache(product.csv_update),
        name="shop_product_csv_update"),
]

# Payment
urlpatterns += [
    url(r'^payment/create/$', payment.create, name="shop_payment_create"),
    #url(r'^payment/capture/$', payment.capture, name="shop_payment_capture"),
    #url(r'^payment/approved/$', payment.approved, name="shop_payment_approved"),
    #url(r'^payment/error/$', payment.error, name="shop_payment_error"),
]

# Etc
urlpatterns += [
    url(r'^cart/recalculate_shipping/$', cart.recalculate_shipping, name="shop_cart_recalculate_shipping"),
]
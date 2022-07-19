from django.conf import settings

SHOP_DEFAULT_CURRENCY = getattr(settings, 'SHOP_DEFAULT_CURRENCY', 'CAD')
CART_SESSION_KEY = getattr(settings, 'SHOP_CART_SESSION_KEY', 'cart_id')
ORDER_SESSION_KEY = getattr(settings, 'SHOP_ORDER_SESSION_KEY', 'order_id')

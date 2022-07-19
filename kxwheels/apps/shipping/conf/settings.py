from django.conf import settings

SHIPPING_MODULES = getattr(settings, 'SHIPPING_MODULES', ('weighted',))

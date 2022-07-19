import os
import sys
import locale
from .conf import settings

'''
from django.conf import settings
settings.configure(
    DEBUG=True, TEMPLATE_DEBUG=True,
    TEMPLATE_DIRS=('/Users/nav/Documents/envs/NavApps/lib/python2.7/site-packages/shipping/templates',),
    INSTALLED_APPS=('shipping',),
)
'''

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

def get_modules():
    """docstring for get_modules"""
    modules = []
    for module in settings.SHIPPING_MODULES:
        try:
            m = sys.modules["kxwheels.apps.shipping.modules.%s" % module]
        except KeyError:
            __import__("kxwheels.apps.shipping.modules.%s" % module)
            m = sys.modules["kxwheels.apps.shipping.modules.%s" % module]
        modules.append(m)
    return modules

def get_unavailable_module():
    try:
        m = sys.modules["kxwheels.apps.shipping.modules.unavailable"]
    except KeyError:
        __import__("kxwheels.apps.shipping.modules.unavailable")
        m = sys.modules["kxwheels.apps.shipping.modules.unavailable"]
    return m
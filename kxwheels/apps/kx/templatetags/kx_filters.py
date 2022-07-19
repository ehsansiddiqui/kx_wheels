from decimal import Decimal
from django import template
from django.utils.translation import to_locale, get_language

try:
    from pytz import timezone
except ImportError:
    timezone = None

babel = __import__('babel', {}, {}, ['core', 'support'])
Format = babel.support.Format
Locale = babel.core.Locale

register = template.Library()


def _get_format():
    locale = Locale.parse(to_locale(get_language()))
    if timezone:
        tzinfo = timezone(settings.TIME_ZONE)
    else:
        tzinfo = None
    return Format(locale, tzinfo)

@register.filter()
def currency(value, currency="CAD"):
    return _get_format().currency(Decimal(value), currency)

@register.filter()
def get_price(product, user):
    if user.is_authenticated and user.is_active:
        return currency(Decimal(product.get_price(user)))
    else:
        return currency(Decimal(product.get_price()))


# Wheelsize fits
def fits(wheelsize, vehicle, place):
    assert place in ['front', 'rear']

    place = getattr(vehicle, "get_%s_wheel_size" % place)
    split = lambda s: [float(i.strip()) for i in s.split(',')]

    dr = split(getattr(place(), 'diameter_range', '0,1000'))
    wr = split(getattr(place(), 'wheelwidth_range', '0,1000'))
    osr = split(getattr(place(), 'offset_range', '-1000,1000'))
    osr = map(lambda n: int(round(float(n))), osr)

    if ((dr[0] <= float(wheelsize.diameter) <= dr[1]) and
        (wr[0] <= wheelsize.wheelwidth <= wr[1]) and
        (osr[0] <= wheelsize.offset <= osr[1])):
        return True
    else:
        return False

def debug_fit(wheelsize, vehicle, place):
    assert place in ['front', 'rear']

    place = getattr(vehicle, "get_%s_wheel_size" % place)
    split = lambda s: [float(i.strip()) for i in s.split(',')]

    dr = split(getattr(place(), 'diameter_range', '0,1000'))
    wr = split(getattr(place(), 'wheelwidth_range', '0,1000'))
    osr = split(getattr(place(), 'offset_range', '-1000,1000'))
    osr = map(lambda n: int(round(float(n))), osr)
    return (('%s'%dr[0] +'<='+ '%s'%float(wheelsize.diameter) +'<='+ '%s'%dr[1]) + ' & ' + 
        ('%s'%wr[0] +'<='+ '%s'%wheelsize.wheelwidth +'<='+ '%s'%wr[1])  + ' & ' + 
        ('%s'%osr[0] +'<='+ '%s'%wheelsize.offset +'<='+ '%s'%osr[1]))

@register.filter()
def debug_front(wheelsizes, vehicle):
    result = '|'
    for size in wheelsizes:
#        if fits(size, vehicle, "front"):
            result = result + '|' + show_fit(size, vehicle, "front")
    return result

@register.filter()
def has_front(wheelsizes, vehicle):
    result = False
    for size in wheelsizes:
        if fits(size, vehicle, "front"):
            result = True
    return result

@register.filter()
def has_rear(wheelsizes, vehicle):
    result = False
    for size in wheelsizes:
        if fits(size, vehicle, "rear") and not fits(size, vehicle, "front"):
            result = True
    return result

@register.filter()
def fits_front(wheelsize, vehicle):
    return fits(wheelsize, vehicle, "front")

@register.filter()
def fits_rear(wheelsize, vehicle):
    return fits(wheelsize, vehicle, "rear")

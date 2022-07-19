import decimal
from django import template
from django.conf import settings
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
def currency(value, currency_format=None):
    if currency_format is None:
        currency_format = getattr(settings, "SHOP_DEFAULT_CURRENCY", "CAD")
    return _get_format().currency(decimal.Decimal(value), currency_format)

@register.filter()
def telephone(value):
    """docstring for telephone"""
    if not value:
        return '-'
    
    # https://gist.github.com/1031560
    # pad the string with 0s until it's at least 10 digits
    string = value
    while len(string) < 10:
        string = "0%s" % string
    string_list = list(string)
    string_list.reverse()
    string = "".join(string_list)

    index = 0
    output_number = ""
    for char in string:
        output_number = "%s%s" % (char, output_number)
        if index == 3:
            output_number = "-%s" % output_number
        elif index == 6:
            output_number = ") %s" % output_number
        elif index == 9:
            output_number = "(%s" % output_number
        index += 1
    
    return output_number

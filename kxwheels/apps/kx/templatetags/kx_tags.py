from django.conf import settings
from urlparse import urlparse, parse_qsl
from django import template
from decimal import Decimal
from django.utils.translation import to_locale, get_language

from kxwheels.apps.kx.models import TireManufacturer, WheelManufacturer

try:
    from pytz import timezone
except ImportError:
    timezone = None
register = template.Library()
babel = __import__('babel', {}, {}, ['core', 'support'])
Format = babel.support.Format
Locale = babel.core.Locale


@register.simple_tag(takes_context=True)
def get_video_thumb(context, url):
    # YouTube only but could be changed to support other providers
    ytkey = dict(parse_qsl(urlparse(url).query))['v']
    thumb = "http://img.youtube.com/vi/{0}/1.jpg".format(ytkey)
    return thumb


@register.simple_tag(takes_context=True)
def get_video_embed_url(context, url):
    # YouTube only but could be changed to support other providers
    ytkey = dict(parse_qsl(urlparse(url).query))['v']
    embed = "http://www.youtube.com/embed/{0}".format(ytkey)
    return embed

# Get manufacturers
class ManufacturerNode(template.Node):
    def __init__(self, parser, token, model):
        self.model = model

    def render(self, context):
        manufacturers = self.model.objects.visible().order_by('name')
        context['manufacturers'] = manufacturers
        return ''

@register.tag
def get_tire_manufacturers(parser, token):
    return ManufacturerNode(parser, token, TireManufacturer)

@register.tag
def get_wheel_manufacturers(parser, token):
    return ManufacturerNode(parser, token, WheelManufacturer)


# Thumbnails
class KxThumbnailNode(template.Node):
    def __init__(self, parser, token):
        bits = token.split_contents()
        if len(bits) < 5 or bits[-2] != "as":
            raise template.TemplateSyntaxError(self.error_msg)
        self.picture = parser.compile_filter(bits[1])
        self.size = parser.compile_filter(bits[2])

        self.as_var = bits[-1]
        self.nodelist_file = parser.parse(('empty', 'endkxthumbnail'))

        if parser.next_token().contents == 'empty':
            self.nodelist_empty = parser.parse(('endkxthumbnail',))
            parser.delete_first_token()

    def render(self, context):
        picture = self.picture.resolve(context)
        size = self.size.resolve(context)

        try:
            thumbnail = picture.thumbnails.get(size=size)
        except:
            thumbnail = object()

        context.push()
        context[self.as_var] = thumbnail
        output = self.nodelist_file.render(context)
        context.pop()

        return output

@register.tag(name='kxthumbnail')
def kxthumbnail(parser, token):
    return KxThumbnailNode(parser, token)

def _get_format():
    locale = Locale.parse(to_locale(get_language()))
    if timezone:
        tzinfo = timezone(settings.TIME_ZONE)
    else:
        tzinfo = None
    return Format(locale, tzinfo)

def currency(value, currency="CAD"):
    return _get_format().currency(Decimal(value), currency)

@register.simple_tag
def get_price(product, user, subdomain):
    return currency(Decimal(product.get_price(user, subdomain)))

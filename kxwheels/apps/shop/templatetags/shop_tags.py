import re
from django import template
from django.views.decorators.cache import never_cache
from django.contrib.sessions.models import Session
from kxwheels.apps.shop.models import Cart, BaseProduct
from kxwheels.apps.shop.forms import AddToCartForm

register = template.Library()


# Add To Cart Tag
class AddToCartNode(template.Node):
    def __init__(self, product, var_name):
        self.product = template.Variable(product)
        self.var_name = var_name
        
    def render(self, context):
        try:
            product = self.product.resolve(context)
            assert isinstance(product, BaseProduct)
            context[self.var_name] = AddToCartForm(product=product)
        except template.VariableDoesNotExist:
            pass
        return ''



@register.tag
def add_to_cart_form(parser, token):
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires arguments" % token.contents.split()[0])
    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError("%r tag had invalid arguments" % tag_name)
    product, var_name = m.groups()
    return AddToCartNode(product, var_name)



# Shopping Cart
@register.inclusion_tag('shop/cart_sidebar.html', takes_context=True)
def cart_sidebar(context):
    request = context['request']
    try:
        cart = Cart.objects.get(pk=request.session.get('cart_id'))
    except Cart.DoesNotExist:
        cart = None
        
    return {'cart': cart}
#TODO: Fix error handling with form. 'err' thing
from datetime import date, timedelta
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string
from django.views.decorators.http import (require_POST, require_GET)
from django.shortcuts import get_object_or_404
from django.contrib.sites.models import Site

from kxwheels.apps.shop.conf import settings
from kxwheels.apps.shop.utils import generate_pdf
from kxwheels.apps.shop.forms import (DiscountCodeForm, ShippingForm, OrderForm, OrderNoteForm, VehicleForm)
from kxwheels.apps.shop.models import (Setting, Order, Item, Discount, CartShipping)
from kxwheels.apps.shop.decorators import (require_staff_or_owner, require_cart, require_order)
from kxwheels.apps.vehicle.models import Model
from kxwheels.context_processors import get_subdomain_owner

def list(request):
    """
    Returns order history of a customer.
    """
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return HttpResponse(render_to_string(request=request,
                                         template_name='shop/base_order_list.html',
                                         context={'orders': orders}, ))

@require_POST
@require_cart
@login_required(redirect_field_name='return_path')
def create(request):
    order_initial = {
        'customer': request.user,
        'dealer': get_subdomain_owner(request),
        'selected_vehicle': '%s' % Model.get_from_cache(request),
        'site': Site.objects.get_current(),
        'status': 0, # Preview
    }
    
    order = Order.objects.create(**order_initial)
    order.convert_from_cart(request.cart)
    order.save()
    
    request.session[settings.ORDER_SESSION_KEY] = order.pk
    return HttpResponseRedirect(reverse('shop_payment_create'))
    
@require_order
def delete(request):
    try:
        order = Order.objects.get(
            pk=request.session.get(settings.ORDER_SESSION_KEY)
        )
    except Order.DoesNotExist:
        pass
    else:
        order.delete()
        
    try:
        del request.session[settings.ORDER_SESSION_KEY]
    except IndexError:
        pass

    return HttpResponseRedirect(request.return_path)
        
@require_GET
@require_staff_or_owner(Order)
def read(request, object_id=None):
    """
    Returns the order based on provided 'id' as a GET request. Only owner of the
    order and users with "Can change order" are allowed.
    """
    format = request.GET.get('fmt', 'html')
    current_site = Site.objects.get_current()
    shop_setting = Setting.objects.get_current()

    context = {'shop_config': shop_setting}
    try:
        order = Order.objects.get(id=object_id)
    except Order.DoesNotExist:
        raise Order.DoesNotExist
    else:
        context['order'] = order
        context['user'] = request.user

    if format=='pdf':
        return generate_pdf(order.id, context, "shop/order_pdf.html")
    else:
        return HttpResponse(render_to_string(request=request,
                                             template_name='shop/base_order.html',
                                             context=context))
            
        
@require_POST
@require_cart
@require_order
def update(request):
    order_form = OrderForm(request.POST, request.FILES)
    discount_code_form = DiscountCodeForm(request.POST, request.FILES)
    shipping_form = ShippingForm(request.cart, request.POST, request.FILES)
        
    err = []
    
    # Discount
    if discount_code_form.is_valid():
        _dc = discount_code_form.cleaned_data.get('discount_code')
        try:
            _discount = Discount.objects.get(code=_dc)
        except Discount.DoesNotExist:
            err.append('Invalid discount code')
        else:
            request.order.discount = _discount.get_amount()
            request.order.save()
    else:
        err.append('Invalid discount code')
        
    # Shipping
    if shipping_form.is_valid():
        _shipping = shipping_form.cleaned_data.get('shipping_option')
        if _shipping:
            request.order.shipping_option = _shipping.name
            request.order.shipping_cost = _shipping.cost
            request.order.save()
        else:
            pass
    else:
        err.append('Invalid shipping')

    return HttpResponseRedirect(reverse('shop_order_summary'))
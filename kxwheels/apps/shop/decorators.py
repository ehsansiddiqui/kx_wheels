from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.contrib.sessions.models import Session
from django.http import (HttpResponseForbidden, 
                        HttpResponseRedirect, 
                        HttpResponseBadRequest)
from kxwheels.apps.shop.conf import settings
from kxwheels.apps.shop.models import Cart, Order

try:
    from functools import update_wrapper, wraps
except ImportError:
    from django.utils.functional import update_wrapper, wraps


def require_staff_or_owner(model=None):
    """
    This decorator will allow access to staff members or the owner of the 
    model. The 'model' must have a foreign key relationship with
    auth.models.User as 'user'. An 'object_id' must be passed to the calling
    view function.    
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            grant = False
            if model and 'object_id' in kwargs:
                object_id = kwargs.get('object_id')
                if object_id is not None:
                    if request.user.is_superuser or request.user.is_staff:
                        grant = True
                    elif request.user == model.objects.get(pk=object_id).user:
                        grant = True
                    else:
                        grant = False
                        
            if grant:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("Error 403: Request forbidden.")
        return wraps(view_func)(_wrapped_view)
    return decorator

def require_cart(view_func):
    """docstring for cart_required"""
    def _decorated(request, *args, **kwargs):

        #TODO: Return path is a bad idea. Get rid of it.
        '''
        # Set return path in request object
        default_return_path = request.META.get('HTTP_REFERER', '/')
        return_path = request.POST.get('return_path', default_return_path)
        setattr(request, "return_path", return_path)
        '''
        setattr(request, "return_path", reverse('shop_cart'))
        
        # Check to see if the cart has already been converted to an order
        if request.session.has_key(settings.ORDER_SESSION_KEY):
            return HttpResponseRedirect(reverse('shop_payment_create'))
        
        # Check cart availability: make one if not available
        cart = Cart.objects.filter(pk=request.session.get(settings.CART_SESSION_KEY))

        if cart.exists():
            cart = cart[0]
        else:
            cart = Cart.objects.create(
                site=Site.objects.get_current(),
                pk=request.session.get(settings.CART_SESSION_KEY),
            )
        
        if request.user.is_authenticated() and request.user.is_active:
            cart.customer = request.user
            cart.customer_email = request.user.email
            cart.save()

        request.session[settings.CART_SESSION_KEY] = cart.pk
        
        setattr(request, "cart", cart)
        return view_func(request, *args, **kwargs)
        
    return _decorated
    
def require_order(view_func):
    def _decorated(request, *args, **kwargs):
        setattr(request, "return_path", reverse('shop_cart'))
        
        # Check order availability: return order if available or show error
        try:
            order = Order.objects.get(
                site=Site.objects.get_current(),
                pk=request.session.get(settings.ORDER_SESSION_KEY)
            )
        except Order.DoesNotExist:
            try: del(request.session[settings.ORDER_SESSION_KEY])
            except: pass
            return HttpResponseRedirect(reverse('shop_cart'))

        setattr(request, "order", order)
        return view_func(request, *args, **kwargs)

    return _decorated
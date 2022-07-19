# TODO: All cart item validations should go into a form
# TODO: Replace HttpResponse with proper output
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import (HttpResponse, HttpResponseRedirect)

from kxwheels.apps.shop.forms import AddToCartForm
from kxwheels.apps.shop.decorators import require_cart
from kxwheels.apps.shop.signals import cart_received_shipping_information
from kxwheels.apps.shop.utils import is_valid_generic_object
from kxwheels.apps.shop.models import (CartItem, ItemOption, ProductOption)

class AddToCartView(TemplateView):
    template_name = ""

    @method_decorator(require_cart)
    def post(self, request, *args, **kwargs):
        form = AddToCartForm(request.POST)

        if form.is_valid():
            content_type = ContentType.objects.get(pk=form.cleaned_data['content_type_id'])
            cartitem = CartItem.objects.create(cart=request.cart, content_type=content_type,
                                               object_id=form.cleaned_data['object_id'],
                                               qty=form.cleaned_data['quantity'],
                                               make = form.cleaned_data['make'],
                                               year = form.cleaned_data['year'],
                                               )


            cartitem.save()

            cartitem._product_cache.make = request.POST['make']
            cartitem._product_cache.year = request.POST['year']
            cartitem.unit_price = cartitem.product.get_price(request.user)
            cartitem.save()

            # Deal with the product options and price adjustments
            opts = []
            for key, value in request.POST.items():

                if key[:6] == "option" and value != '':
                    opts.append((key.split("_")[1], value))

            for opt in opts:
                try:
                    option = cartitem.product.options.get(pk=opt[0])
                except:
                    pass
                else:
                    try:
                        prod_opt = ProductOption.objects.get(option=opt[0], pk=opt[1])
                    except:
                        # For text input
                        item_value = opt[1]
                        price_adjustment = "0.00"
                    else:
                        # For radio or select
                        item_value = prod_opt.value
                        price_adjustment = prod_opt.price_adjustment

                    item_option = ItemOption.objects.create(name=option.name, value=item_value,
                                                            price_adjustment=price_adjustment)
                    item_option.save()

                    cartitem.options.add(item_option)

        if request.is_ajax():
            return HttpResponse("OK")

        return HttpResponseRedirect(request.return_path)

@require_POST
@require_cart
def update(request):
    _post = request.POST.copy()
    object_id = int(_post.get('object_id', 0))
    try:
        quantity = int(_post.get('quantity', 1))
    except ValueError:
        if _post['return_path']:
            return HttpResponseRedirect(_post['return_path'])
        else:
            return HttpResponseRedirect(request.return_path)
    
    try:
        ci = CartItem.objects.get(pk=object_id, cart=request.cart)
    except CartItem.DoesNotExist:
        pass
    else:
        # Delete item if quantity is lower than 1
        if quantity < 1:
            ci.delete()
        else:
            ci.qty = quantity
            ci.save()

        if ci.cart.customer_id:
            cart_received_shipping_information.send(sender=CartItem, instance=ci.cart)
        else:
            pass
    if _post['return_path']:
        return HttpResponseRedirect(_post['return_path'])
    else:
        return HttpResponseRedirect(request.reutrn_path)

@require_cart
def delete(request):
    _post = request.POST.copy()
    object_id = int(_post.get('object_id', 0))

    try:
        ci = CartItem.objects.get(pk=object_id)
    except CartItem.DoesNotExist:
        pass
    else:
        ci.delete()
        if ci.cart.customer_id:
            cart_received_shipping_information.send(sender=CartItem, instance=ci.cart)
        else:
            pass

    return HttpResponseRedirect(request.return_path)

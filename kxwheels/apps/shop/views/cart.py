# TODO: All cart item validations should go into a form
import json
import requests
import Cookie
import os

from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.http import (HttpResponse, HttpResponseRedirect)
from django.utils.decorators import method_decorator
from django.views.decorators.http import (require_GET)
from django.views.generic import TemplateView
from django.template.loader import render_to_string

from xml.etree import ElementTree

from django.views.generic import (TemplateView, DetailView, ListView)

from django.db.models import Q
from ipware.ip import get_ip

from kxwheels.apps.l10n.forms import AddressForm
from kxwheels.apps.kx.models import *
from kxwheels.apps.vehicle.models import *
from kxwheels.apps.shop.conf import settings
from kxwheels.apps.shop.models import (Setting, Order, Item, Discount, CartShipping, CartItem)
from kxwheels.apps.shop.decorators import require_cart
from kxwheels.apps.shop.forms import (BaseAddressFormSet, DiscountCodeForm, ShippingForm, VehicleForm)
from kxwheels.apps.shop.models import (Discount, )
from kxwheels import context_processors
from kxwheels.apps.shop.signals import cart_received_shipping_information
from kxwheels.context_processors import get_subdomain_owner
from kxwheels.apps.vehicle.models import Model
from django.contrib.sites.models import Site
from kxwheels.apps.kx.models import WheelSize as Wheelsize
from kxwheels.apps.shop.listeners import email_order_on_received
from kxwheels.apps.shop.models.cart import OrderLogout
from kxwheels.apps.shop.models.cart import OrderLogoutProductt
from kxwheels.apps.shop.models.order import OrderLoginProduct
from kxwheels.apps.kx.models.accessories import *

from django.core.urlresolvers import reverse
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
from django.db import connection, transaction

def create(request):
    # Let item_create handle it :)
    pass


class ShortSummaryView(TemplateView):
    template_name = "shop/cart_sidebar.html"

    @method_decorator(require_cart)
    def get(self, request, *args, **kwargs):
        if 'json' in request.GET.keys():
            result = {
                'items': request.cart.get_total_items(),
                'subtotal': str(request.cart.get_subtotal()),
            }
            return HttpResponse(json.dumps(result), content_type='application/json')
        else:
            context = self.get_context_data(**kwargs)
            context['cart'] = request.cart
            return self.render_to_response(context)


@require_cart
def read(request):
    cart = request.cart
    AddressFormSet = formset_factory(AddressForm,
        extra=2, formset=BaseAddressFormSet)
    context = { 'cart': cart,}

    if request.method == 'GET':
        discount_code_form = DiscountCodeForm()
        address_formset = AddressFormSet(initial=[
            cart.billing_address,
            cart.shipping_address
        ])
        shipping_form = ShippingForm(cart=cart)
        if cart.shipping_quotes.filter(is_selected=True).count() > 0:
            cart.shipping_quotes.exclude(is_selected=True).delete()
            shipping_form.fields['shipping_option'].queryset = shipping_form.fields['shipping_option'].queryset.exclude(is_selected=False)

    elif request.method == 'POST':
        is_addr_valid, is_disc_valid, is_ship_valid = (False,)*3

        # Address forms
        address_formset = AddressFormSet(request.POST, request.FILES)
        if address_formset.is_valid():
            billing_address_form = address_formset[0]
            shipping_address_form = address_formset[1]

            for key, val in billing_address_form.cleaned_data.items():
                key = "billing_%s" % key
                try:
                    setattr(cart, cart._meta.get_field(key).name, val)
                except:
                    # Field Does Not exist
                    pass

            for key, val in shipping_address_form.cleaned_data.items():
                key = "shipping_%s" % key
                try:
                    setattr(cart, cart._meta.get_field(key).name, val)
                except:
                    # Field Does Not Exist
                    pass

            # Special case
            setattr(cart, 'billing_phone', billing_address_form.cleaned_data['landline_phone'])
            setattr(cart, 'shipping_phone', shipping_address_form.cleaned_data['landline_phone'])

            is_addr_valid = True

        # Discount form
        discount_code_form = DiscountCodeForm(request.POST, request.FILES)
        if discount_code_form.is_valid():
            dc = discount_code_form.cleaned_data.get('code')
            if dc:
                discount = Discount.objects.get(code=dc)
                cart.discount = discount
            is_disc_valid = True

        cart.shipping_quotes.filter(is_selected=True).delete()

        # Shipping form
        shipping_form = ShippingForm(request.POST, cart=cart)

        # subdomain = context_processors.extract_subdomain(request)['subdomain']
        #
        # if subdomain:
        #     is_ship_valid = True

        if shipping_form.is_valid():
            so = shipping_form.cleaned_data.get('shipping_option')
            if so:
                for sq in cart.shipping_quotes.filter(is_selected=True):
                    sq.is_selected = False
                    sq.save()
                so.is_selected = True
                so.save()
            is_ship_valid = True

        if not all([is_addr_valid, is_disc_valid, is_ship_valid]):
            cart.shipping_quotes.all().delete()
            cart_received_shipping_information.send(sender=cart.__class__, instance=cart)
            cart.save()
        else:
            cart.shipping_quotes.exclude(is_selected=True).delete()
            cart.save()
            shipping_form.fields['shipping_option'].queryset = shipping_form.fields['shipping_option'].queryset.exclude(is_selected=False)
            return HttpResponseRedirect(reverse('shop_cart_summary'))

    context['discount_code_form'] = discount_code_form
    context['address_formset'] = address_formset
    context['shipping_form'] = shipping_form
    return HttpResponse(render_to_string(request=request,
                                         template_name='shop/cart_detail.html',
                                         context=context))

@require_cart
def order_add(request):
    cart = request.cart

    if cart.customer:
        order_initial = {
            'customer': request.user,
            'dealer': get_subdomain_owner(request),
            'selected_vehicle': '%s' % Model.get_from_cache(request),
            'site': Site.objects.get_current(),
            'status': 1,  # Preview
        }

        order = Order.objects.create(**order_initial)
        for p in request.cart.items.all():
            product = {
                'product': p.product.name,
                'make': p.make,
                'year': p.year,
                'model': p.product.model,
                'order_id': order.id
            }
            orderproduct = OrderLoginProduct.objects.create(**product)
        order.convert_from_cart(request.cart)
        order.save()



        request.session[settings.ORDER_SESSION_KEY] = order.pk

        try:
            del request.session[settings.CART_SESSION_KEY]
        except IndexError:
            pass
    else:
        product_name = []
        for item in request.cart.items.all():
            product_name.append(item.product.name)


        ip = get_ip(request)
        if request.cart.items.all():
            order = OrderLogout(
                status='completed',  # Preview
                price=request.cart.get_total(),
                name=request.cart.billing_first_name + '' + request.cart.billing_last_name,
                address=request.cart.billing_address_1,
                cart_id=request.cart.id,
                email=request.COOKIES.get('email'),
                created_at=request.cart.created_at,
                ip_address=ip,
            )
            order.save()
            for p in request.cart.items.all():
                product = {
                    'product': p.product.name,
                    'make': p.make,
                    'year': p.year,
                    'model': p.make,
                    'orderlogout_id': order.id
                }
                orderproduct = OrderLogoutProductt.objects.create(**product)

            request.cart.delete()
        else:
            pass

@require_cart
def success(request):

    order_add(request)

    return HttpResponse(render_to_string(request=request,
                                         template_name='shop/success.html',
                                         ))

@require_cart
def delete(request):
    try:
        del request.session[settings.CART_SESSION_KEY]
    except IndexError:
        pass
    return HttpResponseRedirect(request.return_path)



def accessories_view(request):
    # os.system('python manage.py export_dealer_data' )
    template_name = 'shop/cart_detail.html'
    accessories = AccessoriesList.objects.all().order_by('id')
    list_range = 4 * len(accessories)
    data_list = [0 for x in range(list_range)]
    j = 0
    for access in accessories:
        data_list[j] = access.id
        data_list[j+1] = access.name
        accessories_picture = AccessoriesPicture.objects.filter(wheel_id = access.id).order_by('wheel_id')
        for pic in accessories_picture:
            pic_path = AccessoriesPictureThumbnail.objects.values('path').filter(wheelpicture_id=pic.id, size='lg')
            data_list[j + 2] = pic_path[0]['path']
        accessories_price = AccessoriesDetail.objects.values('price').filter(accessories_list_id=data_list[j]).order_by('accessories_list_id').distinct('accessories_list_id')
        data_list[j + 3] = str(accessories_price[0]['price'])
        j = j + 4

    response = HttpResponse(json.dumps(data_list), content_type='Application/json')
    return response



@require_cart
def email_details(request):
    template_name = 'shop/cart_summary.html'
    cart = request.cart
    data_list = request.POST['val']
    order_add.email = data_list
    response = HttpResponse(json.dumps(data_list), content_type='Application/json')
    response.set_cookie('email', data_list)

    return response



@require_cart
def recalculate_shipping(request):
    request.cart.shipping_quotes.all().delete()
    request.cart.shipping_option = None
    request.cart.shipping_cost = '0.00'
    request.cart.save()

    return HttpResponseRedirect(request.return_path)


@require_GET
@require_cart
def summary(request):
    cart = request.cart

    discount_code_form = DiscountCodeForm()
    shipping_form = ShippingForm(cart=cart)

    product_name = []
    for items in cart.items.all():

        product_name.append(items.product.name)

    paypal_dict = {

        "business": "useryahoo786-facilitator@gmail.com",
        #"amount": cart.get_total(),
		"amount": '0.01',
        "item_name": '',
        "Quantity": cart.get_total_items(),
        "invoice": cart.id,
        "notify_url": 'http://old.kxwheels.com/shop/cart/',
        "return_url": 'http://old.kxwheels.com/shop/cart/success/',
        "cancel_return": 'http://old.kxwheels.com/shop/cart/',
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }
    for name in product_name:
        if paypal_dict['item_name']:
            paypal_dict['item_name'] = paypal_dict['item_name'] + "  '  " + name
        else:
            paypal_dict['item_name'] = name


    # Accessories_list_details

    accessories_name = []
    accessories_price  = []
    accessories_url  = []
    accessories = AccessoriesList.objects.all()
    for accessorie in accessories:
        picture =  AccessoriesPicture.objects.filter(wheel_id = accessorie.id)
        for pictures in picture:
            accessories_url.append(pictures.picture)
        acc_detail = AccessoriesDetail.objects.filter(accessories_list_id=accessorie.id)
        for acc_details in acc_detail:
            accessories_name.append(accessorie.name)
            accessories_price.append(acc_details.price)

    accessories_detail = [accessories_name, accessories_price, accessories_url]

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {
        'cart': cart,
        'discount_code_form': discount_code_form,
        'shipping_form': shipping_form,
        'form': form,
        'accessories_detail': accessories_detail,
    }



    return HttpResponse(render_to_string(request=request,
                            template_name='shop/cart_summary.html',
                            context=context))

@require_cart
def card_success(request):

    card_num = request.POST['card_num']
    cvv = request.POST['cvv']
    expiry_date = request.POST['expiry']
    if request.POST['u_name']:
        name = request.POST['u_name']
    else:
        name = ''
    if request.POST['address']:
        address = request.POST['address']
    else:
        address = ''

    # API URL
    if card_num and cvv and expiry_date:
        url = "https://secure.myhelcim.com/api/"

        # POST DATA
        postData = {

            'accountId': '2500338158',
            'apiToken': 'gY68MXPW5PCrM5D6xgjT4c98d',
            'transactionType': 'purchase',
            # 'terminalId': '7',
            'test': '1',
            'amount': '5.00',
            'cardHolderName': name,
            'cardNumber': card_num,
            'cardExpiry': expiry_date,
            'cardCVV': cvv,
            'cardHolderAddress': address,
            # 'cardHolderPostalCode': '90212',
            "transactionType": "preauth" ,

        }

        # POST
        response = requests.post(url, data=postData)


        # GET XML RESPONSE
        xmlResponse = ElementTree.fromstring(response.content)

        if xmlResponse._children[0].text == '1' and xmlResponse._children[1].text == 'APPROVED':
            context = {
                'response': response.text
            }

            order_add(request)
            return HttpResponse(render_to_string(request=request,
                                                 template_name='shop/success_card.html',
                                                 context=context))
        else:

            context = {
                'error' : xmlResponse._children[1].text
            }
            return HttpResponse(render_to_string(request=request,
                                                 template_name='shop/cart_summary.html',
                                                 context=context))
    else:
		pass




















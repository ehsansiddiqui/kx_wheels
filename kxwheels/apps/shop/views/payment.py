from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site

from kxwheels.apps.remittance.modules.beanstream import Emption
from kxwheels.apps.remittance.models import Seller, Buyer, Purchase, PurchaseItem
from kxwheels.apps.shop.decorators import (require_order)
from kxwheels.apps.shop.templatetags import shop_filters


@login_required
@require_order
def create(request):
    """docstring for create"""
    
    order = request.order
    current_site = Site.objects.get_current()
    shop_setting = current_site.shop_setting
    
    seller = Seller(
        company_name=shop_setting.store_name,
        address_1=shop_setting.street1,
        address_2=shop_setting.street2,
        city=shop_setting.city,
        province=shop_setting.province,
        postal_code=shop_setting.postal_code,
        country=shop_setting.country,
        phone=shop_setting.phone,
        email=shop_setting.store_email,
    )
    
    buyer = Buyer(
        customer=order.customer,
        email=order.customer_email,
        billing_first_name=order.billing_first_name,
        billing_last_name=order.billing_last_name,
        billing_address_1=order.billing_address_1,
        billing_address_2=order.billing_address_2,
        billing_city=order.billing_city,
        billing_province=order.billing_province,
        billing_postal_code=order.billing_postal_code,
        billing_country=order.billing_country,
        billing_phone=order.billing_phone,
        
        shipping_first_name=order.shipping_first_name,
        shipping_last_name=order.shipping_last_name,
        shipping_address_1=order.shipping_address_1,
        shipping_address_2=order.shipping_address_2,
        shipping_city=order.shipping_city,
        shipping_province=order.shipping_province,
        shipping_postal_code=order.shipping_postal_code,
        shipping_country=order.shipping_country,
        shipping_phone=order.shipping_phone,
    )
    
    purchase = Purchase(
        order=order.pk,
        subtotal=order.get_subtotal(),
        tax=order.get_tax(),
        shipping=order.get_shipping_summary()[2],
        discount=order.get_discount_summary()[1],
        total=order.get_total(),
        note=order.customer_notes,
        currency='CAD',
    )


    purchase_items = list()
    for oi in order.items.all():
        prep_item_name = [oi.product.name]
        for item in oi.options.all():
            option = '%s=%s' % (item.name, item.value)
            if item.price_adjustment:
                option += ' (%s)' % shop_filters.currency(item.price_adjustment)
            prep_item_name.append(option)
            
        pi = PurchaseItem(
            sku=oi.product.sku,
            name='\n'.join(prep_item_name),
            desc=oi.product.short_desc,
            qty=oi.qty,
            unit_price=oi.get_price(),
            discount='-0.00',
            ext_price=oi.get_extended_price(),
            tax='0.00', # Will get it later
        )
        purchase_items.append(pi)
    
    return Emption(request, seller, buyer, purchase, purchase_items)

'''
def capture(request):
    context = {}

    if request.method == "POST":
        capture_form = CaptureForm(request.POST)

        if capture_form.is_valid():
            order_id = capture_form.cleaned_data.get('order_id')
            trans_id = capture_form.cleaned_data.get('trans_id')
            amount = capture_form.cleaned_data.get('amount')

            return Capture(order_id, trans_id, amount)
        else:
            return HttpResponse('Invalid request')
    else:
        payment_id = request.GET.get('payment_id', None)
        if payment_id is not None:
            payment = get_object_or_404(Payment, pk=payment_id)
            _dict = {
                'order_id':payment.order.pk,
                'trans_id':payment.trans_id,
                'amount':payment.amount,
            }
        
        capture_form = CaptureForm(initial=_dict)
        
    context['capture_form'] = capture_form
    return direct_to_template(request, 'shop/capture.html', context)

def approved(request):
    trans_id = request.GET.get('id', None)
    context = {}
    if trans_id is not None:
        payment = Payment.objects.get(pk=trans_id)
        context['payment'] = payment
        
        current_site = Site.objects.get_current()
        shop_setting = current_site.shop_setting
        context['site'] = shop_setting
        
        # Remove order from session
        try:del(request.session[settings.ORDER_SESSION_KEY])
        except KeyError:pass
        
    return direct_to_template(request, 'shop/payment_approved.html', context)

def error(request):
    return HttpResponse('Error occured while processing your payment.')
'''

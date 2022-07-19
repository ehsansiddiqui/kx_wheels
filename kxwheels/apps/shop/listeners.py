from django.conf import settings
from django.contrib.sites.models import Site
from django.db.models import signals

from kxwheels.apps.remittance import signals as remittance_signals
from kxwheels.apps.shop import signals as shop_signals
from kxwheels.apps.shop.models import (Setting, Order, Cart,
                                       CartShipping, CartItem, Payment)


def record_payment(sender, instance, **kwargs):
    preauth = instance
    try:
        order = Order.objects.get(pk=preauth.order_id)
    except Order.DoesNotExist:
        #raise "Payment for non-existing order"
        return False
    
    payment, created = Payment.objects.get_or_create(
        order=order, trans_id=preauth.trans_id, 
        trans_datetime=preauth.trans_datetime,
    )
    if created:
        payment.trans_type = preauth.trans_type
        payment.amount = preauth.amount
        payment.method = preauth.method
        payment.gateway =  preauth.gateway
        payment.auth_code = preauth.auth_code
        payment.iso_code = preauth.iso_code
        payment.response_code = preauth.response_code
        payment.reason_code = preauth.reason_code
        payment.message = preauth.message
        payment.is_success = preauth.is_success
        payment.raw = preauth.raw
        payment.save()

def sync_prodattrs(sender, instance, **kwargs):
    """docstring for sync_prod_attrs"""
    """
    _optsets = instance.optsets.all()
    _options = Option.objects.filter(set__in=_optsets)
    for opt in _options:
        prodattr, created = ProductOption.objects.get_or_create(
            option=opt,
            content_type=ContentType.objects.get_for_model(instance.__class__),
            object_id=instance.pk,
        )
        if created:
            prodattr.save()
            
    _orphaned_prodattrs = ProductOption.objects.filter(
        ~Q(option__set__in=_optsets)
    )
    if _orphaned_prodattrs:
        _orphaned_prodattrs.delete()
    """
    pass
    
def populate_shipping_quotes(sender, instance, **kwargs):
    '''
    if not instance.items.all():
        return False

    if not instance.shipping_postal_code:
        return False
    '''

    if not instance.is_valid_shipping_address():
        return

    from kxwheels.apps.shipping import get_modules, get_unavailable_module
    from kxwheels.apps.shipping.models import Seller, Buyer, Parcel, ParcelItem
    
    current_site = Site.objects.get_current()
    shop_setting = current_site.shop_setting
    seller = Seller(
        name=shop_setting.store_name,
        address=shop_setting.street1,
        city=shop_setting.city,
        province=shop_setting.province,
        postal_code=shop_setting.postal_code,
        country=shop_setting.country,
        phone=shop_setting.phone,
        email=shop_setting.store_email,
    )
    # if instance.customer_id is None:
    #     name = instance.billing_first_name + instance.billing_last_name
    # else:
    #     name = instance.customer.get_full_name()
    buyer = Buyer(
        name=instance.customer.get_full_name() if instance.customer else instance.billing_first_name + instance.billing_last_name,
        address=instance.shipping_address_1,
        city=instance.shipping_city,
        province=instance.shipping_province,
        postal_code=instance.shipping_postal_code,
        country=instance.shipping_country,
        phone=instance.shipping_phone,
        email=instance.customer_email,
    )

    parcel = Parcel()
    
    for ci in instance.items.all():
        pi = ParcelItem(
            name=ci.product,
            qty=ci.qty,
            unit_price=ci.get_price(),
            weight=(ci.product.weight, ci.product.weight_unit),
            length=(ci.product.length, ci.product.length_unit),
            width=(ci.product.width, ci.product.width_unit),
            height=(ci.product.height, ci.product.height_unit),
        )
        parcel.add_item(pi)

    # Clear current quotes
    _current_shipping_quotes = CartShipping.objects.filter(cart=instance)
    _current_shipping_quotes.delete()
    
    shipping_modules = get_modules()

    for module in shipping_modules:
        shipper = module.Shipper(seller=seller, buyer=buyer, parcel=parcel)

        try:
            products = shipper.products()
        except Exception as e:
            shipping_module = get_unavailable_module()
            shipper = shipping_module.Shipper(seller=seller, buyer=buyer, parcel=parcel)

            for product in shipper.products():
                cartshipping = CartShipping.objects.create(
                    cart=instance,
                    name=product.name,
                    days=product.days,
                    cost=product.rate,
                )
                cartshipping.save()

        else:
            for product in products:
                cartshipping = CartShipping.objects.create(
                    cart=instance,
                    name=product.name,
                    days=product.days,
                    cost=product.rate,
                )
                cartshipping.save()

def clear_shipping_quotes(sender, instance, **kwargs):
    instance.cart.shipping_quotes.all()


def email_order_on_received(sender, instance, **kwargs):
    order = instance.items.product.name
    from django.core.mail import EmailMessage
    from django.template import loader, Context

    current_site = Site.objects.get_current()
    shop_setting = Setting.objects.get_current()
    email_context = {
        'subject': "Order %s - Your Paramount Tire order." % order.id,
        'sender': settings.DEFAULT_FROM_EMAIL,
        'phone': shop_setting.phone,
        'recipient': (order.user.email,settings.ADMIN_EMAIL),
        'site': current_site,
        'order': order, 
    }

    template = loader.get_template('shop/order_email.txt')
    email = EmailMessage(
        subject = email_context['subject'],
        body = template.render(Context(email_context,)), 
        from_email = email_context['sender'],
        to = email_context['recipient'],
        bcc = (email_context['sender'], shop_setting.store_orders_email,)
    )
    email.send(fail_silently=False)

def start_listening():
    """Add required listeners"""
    #QR Code disabled in favour of ReportLab's inbuilt CODE39 barcode
    #signals.post_save.connect(generate_qrcode, sender=Order)
    shop_signals.order_received.connect(email_order_on_received)
    #shop_signals.product_save.connect(sync_prodattrs)
    
    signals.post_save.connect(clear_shipping_quotes, sender=CartItem)
    signals.pre_delete.connect(clear_shipping_quotes, sender=CartItem)
    shop_signals.cart_received_shipping_information.connect(populate_shipping_quotes)
    remittance_signals.preauth_received.connect(record_payment)

    # signals.post_save.connect(populate_shipping_quotes, sender=Cart)


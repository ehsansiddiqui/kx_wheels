from datetime import date, timedelta
from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from kxwheels.apps.l10n.models import AdminArea
from kxwheels.apps.shop.models import (Collection, Item, Cart,)
from kxwheels.apps.shop import signals as shop_signals

class Order(Collection):
    STATUS_CHOICES = (
        (0, 'Preview'),
        (1, 'Received'),
        (2, 'In Process'),
        (3, 'Completed'),
        (4, 'Declined'),
    )
    site = models.ForeignKey(Site, verbose_name=_("site"), related_name="orders")
    customer = models.ForeignKey(User, verbose_name=_("customer"), related_name='orders')
    dealer = models.ForeignKey(User, verbose_name=_("dealer"), related_name='dealers', null=True, blank=True)
    discount = models.DecimalField(_("discount"), max_digits=16, decimal_places=4, default='0.00')
    shipping_option = models.CharField(_("shipping option"), max_length=255, blank=True, null=True)
    shipping_cost = models.DecimalField(_("shipping cost"), max_digits=16, decimal_places=4, default='0.00')
    shipping_delivery = models.DateField(_("shipping delivery"), blank=True, null=True)
    selected_vehicle = models.CharField(_("selected vehicle"), max_length=255, blank=True, null=True)
    make = models.CharField(_("make"), max_length=255, blank=True, null=True)
    year = models.CharField(_("year"), max_length=255, blank=True, null=True)

    dealer.nullfilter = True
    
    # Shipping and Billing fields are defined in collection.py.
    customer_notes = models.TextField(blank=True, null=True)
    po = models.CharField(_("purchase order"), max_length=100, blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0, blank=True)
    
    class Meta:
        verbose_name = "order"
        verbose_name_plural = "orders"
        app_label = 'shop'

    def __unicode__(self):
        return "%s" % self.pk

    @models.permalink
    def get_absolute_url(self):
        return ('shop_order_read', [self.pk])
    
    def convert_from_cart(self, cart):
        assert isinstance(cart, Cart)
        if cart.get_total_items() < 1:
            self.delete()
            return False

        # Clear order items, if they are there
        _oi = OrderItem.objects.filter(order=self)
        _oi.delete()
        
        # Copy cart details
        for field in cart._meta.fields:
            if field.name in ["id", "cart_id", "customer"]: pass
            else: setattr(self, field.name, getattr(cart, field.name))

        if cart.discount:
            self.discount = cart.get_discount_summary()[1]
        else:
            self.discount = '0.0'

        # Copy Shipping
        shipping = cart.get_shipping_summary()
        if shipping and shipping[0]:
          self.shipping_option = shipping[0]
          self.shipping_delivery = date.today()+timedelta(days=shipping[1])
          self.shipping_cost = shipping[2]

        self.save()
        
        # Copy cart items
        cart_items = cart.items.all()
        for item in cart_items:
            assert isinstance(item, Item)
            oi = OrderItem(order=self)
            for field in item._meta.fields:
                if field.name in ["id", "cart_id",]: pass
                else: setattr(oi, field.name, getattr(item, field.name))
            oi.save()
            
            # Copy cart item options
            for opt in item.options.all():
                oi.options.add(opt)
            oi.save()
            item.delete()
        
        cart.delete()
        #shop_signals.order_received.send(sender=Order, instance=self)
        
    def get_discount_summary(self):
        return ('Discount', self.discount)
        
    def get_shipping_summary(self):
        return (
            self.shipping_option, 
            self.shipping_delivery, 
            self.shipping_cost
        )
    
class OrderItem(Item):
    order = models.ForeignKey('order', verbose_name=_('order'), related_name='items')

    class Meta:
        verbose_name = 'order item'
        verbose_name_plural = 'order items'
        app_label = 'shop'

    def __unicode__(self):
        try:
            return self.product.name
        except:
            return str(self.order)

class OrderNote(models.Model):
    order = models.ForeignKey(Order, verbose_name=_("order"), 
        related_name='notes')
    created_by = models.ForeignKey(User, verbose_name=_("created by"), 
        related_name='owned_order_notes')
    note = models.TextField(_("note"), blank=True, null=True)
    notify_customer = models.BooleanField(_('notify customer?'), default=False)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    
    class Meta:
        app_label = 'shop'
    
    def __unicode__(self):
        try:
            return "%s - %s" % (self.created_by, self.created_at)
        except:
            return str(self.created_at)



class OrderLoginProduct(models.Model):
    order = models.ForeignKey('order', verbose_name=_('order'), related_name='order_login')
    product = models.CharField(_('product'), max_length=255, blank=True, null=True)
    make= models.CharField(_('make'), max_length=255, blank=True, null=True)
    year= models.CharField(_('year'), max_length=255, blank=True, null=True)
    model= models.CharField(_('model'), max_length=255, blank=True, null=True)
    # model= models.CharField(_('ip_address'), max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'shoplogin'
        verbose_name_plural = 'shopslogin'
        app_label = 'shop'

    def __unicode__(self):
        return unicode(self.product)

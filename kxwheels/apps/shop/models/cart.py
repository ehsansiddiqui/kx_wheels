import random
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.sessions.models import Session
from django.utils.translation import ugettext_lazy as _

from kxwheels.apps.shop import signals as shop_signals
from kxwheels.apps.shop.models import Collection, Item, Discount

class Cart(Collection):
    customer = models.ForeignKey(User, verbose_name=_("customer"), 
        related_name='carts', blank=True, null=True)
    discount = models.ForeignKey(Discount, verbose_name=_("discount"), blank=True, null=True)
    site = models.ForeignKey(Site, verbose_name=_("site"), related_name="carts")

    class Meta:
        verbose_name = "cart"
        verbose_name_plural = "carts"
        app_label = 'shop'
    
    def __unicode__(self):
        return unicode(self.created_at)
    
    def get_discount_summary(self):
        if self.discount is None:
            return ('Discount', Decimal('0.00'))
            
        if self.is_valid_shipping_address():
            amount = self.discount.get_amount(self.get_grandtotal())
            if amount > self.get_grandtotal():
                amount = (self.get_grandtotal()*-1)
        else:
            amount = self.discount.get_amount(self.get_subtotal())
            if amount > self.get_subtotal():
                amount = (self.get_subtotal()*-1)
                
        if amount:
            return ("Discount", amount)
        else:
            return ('Discount', Decimal('0.00'))
            
    def get_shipping_summary(self):
        if self.shipping_quotes:
            for quote in self.shipping_quotes.all():
                if quote.is_selected:
                    return (quote.name, quote.days, quote.cost)
        return (None, None, Decimal('0.00'))
        
class CartItem(Item):
    cart = models.ForeignKey('cart', verbose_name=_('cart'), related_name='items')
    make = models.CharField(_('make'), max_length=255, blank=True, null=True)
    year = models.CharField(_('year'), max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'cart item'
        verbose_name_plural = 'cart items'
        app_label = 'shop'
        
    def __unicode__(self):
        return unicode(self.product)
        
class CartShipping(models.Model):
    cart = models.ForeignKey('cart', verbose_name=_('cart'), related_name='shipping_quotes')
    name = models.CharField(_('shipping option'), max_length=255, blank=True, null=True)
    cost = models.DecimalField(_('shipping cost'), max_digits=16, decimal_places=4, 
        blank=True, null=True)
    days = models.IntegerField(_('delivery days'), blank=True)
    is_selected = models.BooleanField(_('is selected?'), default=False)

    class Meta:
        verbose_name = 'cart shipping'
        verbose_name_plural = 'cart shippings'
        app_label = 'shop'
        
    def __unicode__(self):
        name = self.name
        if 'PurolatorGround' in name:
            name = 'Ground'
        name = "$%.2f - %s" % (self.cost, name)
        if self.days:
            name = "%s (%s day(s))" % (name, self.days)
        return name


class OrderLogout(models.Model):
    # product = models.CharField(_('product'), max_length=255, blank=True, null=True)
    status = models.CharField(_('status'), max_length=255, blank=True, null=True)
    price= models.CharField(_('price'), max_length=255, blank=True, null=True)
    name= models.CharField(_('name'), max_length=255, blank=True, null=True)
    address= models.CharField(_('address'), max_length=255, blank=True, null=True)
    cart_id= models.CharField(_('cart_id'), max_length=255, blank=True, null=True)
    created_at= models.CharField(_('created_at'), max_length=255, blank=True, null=True)
    ip_address= models.CharField(_('ip_address'), max_length=255, blank=True, null=True)
    email= models.CharField(_('email'), max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'shoplogout'
        verbose_name_plural = 'shopslogout'
        app_label = 'shop'

    def __unicode__(self):
        return unicode(self.product)


class OrderLogoutProductt(models.Model):
    orderlogout = models.ForeignKey('orderlogout', verbose_name=_('shoplogout'), related_name='order_product')
    product = models.CharField(_('product'), max_length=255, blank=True, null=True)
    make= models.CharField(_('make'), max_length=255, blank=True, null=True)
    year= models.CharField(_('year'), max_length=255, blank=True, null=True)
    model= models.CharField(_('model'), max_length=255, blank=True, null=True)
    # model= models.CharField(_('ip_address'), max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'shoplogout'
        verbose_name_plural = 'shopslogout'
        app_label = 'shop'

    def __unicode__(self):
        return unicode(self.product)
#TODO: Fix the province hack
#TODO: Make discount a curreny field not a foreign key
import random
from decimal import Decimal

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

# For tax purposes
from kxwheels.apps.l10n.models import AdminArea

class Collection(models.Model):
    # Concrete models must implement site and customer fields with related name
    id = models.IntegerField(_('id'), primary_key=True)
    #discount = models.DecimalField(_("discount"), max_digits=16, decimal_places=4, default='0.00')
    customer_email = models.CharField(_("customer email"), max_length=255, blank=True)

    billing_first_name = models.CharField(_("billing first name"), max_length=255, blank=True)
    billing_last_name = models.CharField(_("billing last name"), max_length=255, blank=True)
    billing_address_1 = models.CharField(_("billing address line 1"), max_length=255, blank=True)
    billing_address_2 = models.CharField(_("billing address line 2"), max_length=255, blank=True)
    billing_city = models.CharField(_("billing city"), max_length=255, blank=True)
    billing_province = models.CharField(_("billing province"), max_length=100, blank=True)
    billing_postal_code = models.CharField(_("billing postal code"), max_length=20, blank=True)
    billing_country = models.CharField(_("billing country"), max_length=100, blank=True)
    billing_phone = models.CharField(_("billing phone"), max_length=20, blank=True)
    
    shipping_first_name = models.CharField(_("shipping first name"), max_length=255, blank=True)
    shipping_last_name = models.CharField(_("shipping last name"), max_length=255, blank=True)
    shipping_address_1 = models.CharField(_("shipping address line 1"), max_length=255, blank=True)
    shipping_address_2 = models.CharField(_("shipping address line 2"), max_length=255, blank=True)
    shipping_city = models.CharField(_("shipping city"), max_length=255, blank=True)
    shipping_province = models.CharField(_("shipping province"), max_length=100, blank=True)
    shipping_postal_code = models.CharField(_("shipping postal code"), max_length=20, blank=True)
    shipping_country = models.CharField(_("shipping country"), max_length=100, blank=True)
    shipping_phone = models.CharField(_("shipping phone"), max_length=20, blank=True)

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    # make = models.CharField(_('make'), max_length=256)
    # year = models.CharField(_('year'), max_length=256)
    # model = models.CharField(_('model'), max_length=256)
    
    class Meta:
        verbose_name = "collection"
        verbose_name_plural = "collections"
        app_label = 'shop'
        abstract = True
        
    def save(self, *args, **kwargs):
        if not self.pk:
            rndnum = random.randrange(11111111,99999999,1)
            self.pk = rndnum
        super(Collection, self).save(*args, **kwargs)


    '''
    def save(self, *args, **kwargs):
        if self.shipping_postal_code:
            try:
                _postal_code = PostalCode.objects.get(postal_code=self.shipping_postal_code)
            except PostalCode.DoesNotExist:
                pass
                # (WTF, why did i do this?) self.shipping_postal_code = None
            else:
                self.shipping_city = _postal_code.city.name
                self.shipping_province = _postal_code.iso_3166_2.iso_3166_2
                self.shipping_country = _postal_code.iso_3166_2.iso_3166_1.name
        
        super(Collection, self).save(*args, **kwargs)
    '''
    
    @property
    def billing_address(self):
        return {
            'first_name': self.billing_first_name,
            'last_name': self.billing_last_name,
            'address_1': self.billing_address_1,
            'address_2': self.billing_address_2,
            'city': self.billing_city,
            'province': self.billing_province,
            'postal_code': self.billing_postal_code,
            'country': self.billing_country,
            'phone': self.billing_phone,
        }
        
    @property
    def shipping_address(self):
        return {
            'first_name': self.shipping_first_name,
            'last_name': self.shipping_last_name,
            'address_1': self.shipping_address_1,
            'address_2': self.shipping_address_2,
            'city': self.shipping_city,
            'province': self.shipping_province,
            'postal_code': self.shipping_postal_code,
            'country': self.shipping_country,
            'phone': self.shipping_phone,
        }

    def __len__(self):
        try:
            count = self.items.count()
        except ValueError:
            count = 0
        return count
        
    def get_billing_full_name(self):
        return u"%s %s" % (self.billing_first_name, self.billing_last_name)

    def get_shipping_full_name(self):
        return u"%s %s" % (self.shipping_first_name, self.shipping_last_name)

    def is_valid_shipping_address(self):
        """docstring for is_valid_shipping_address"""
        if not self.shipping_address_1:
            return False
        elif not self.shipping_city:
            return False
        elif not self.shipping_province:
            return False
        elif not self.shipping_postal_code:
            return False
        elif not self.shipping_country:
            return False
        else:
            return True
        
    def get_total_items(self):
        """Total number of items in the collection"""
        qty = 0
        for item in self.items.all():
            qty += item.qty
        return int(qty)

    def get_subtotal(self):
        subtotal = 0
        for item in self.items.all():
            subtotal += item.get_extended_price()
        return subtotal        
                    
    def get_tax_summary(self):
        assert self.shipping_province is not None
        try:
          _tax_zone = AdminArea.objects.get(iso_3166_2=self.shipping_province)
        except AdminArea.DoesNotExist:
          return []

        # Get a list of tax summary of each product.
        items = [item.get_tax_summary(_tax_zone) for item in self.items.all()]

        # Make one list out of many sublists
        unified_list = []
        for item in items:
            if isinstance(item, list):
                for subitem in item:
                    unified_list.append(subitem)
            else:
                unified_list.append(item)


        # Find out unique tax classes from the list and assignment them zero
        taxes = {}
        for i in unified_list:
            taxes[i[0]] = 0

        # To the unique classes, add the tax amount.
        for i in unified_list:
            taxes[i[0]] = taxes[i[0]] + i[1]

            
        # Rearrange taxes dictionary to be consistent with product tax summary
        tax_summary = []
        for key, val in taxes.items():
            tax_summary.append((key, val))
        
        return tax_summary
    
    def get_tax(self):
        return sum([val for key, val in self.get_tax_summary()])
    
    def get_grandtotal(self):
        return self.get_subtotal() + self.get_tax()

    '''
    Moved to cart.py model
    def get_discount_summary(self):
        _discount_amount = self.discount.get_amount(self.get_grandtotal())
        if _discount_amount:
            if _discount_amount > self.get_grandtotal():
                _discount_amount = (self.get_grandtotal()*-1)

            discount_summary = (
                "Discount", 
                _discount_amount
            )
            return discount_summary
        else:
            return ('Discount', Decimal('0.00'))
    '''
    def get_discount_summary(self):
        # Children must implement this
        return ('Discount', Decimal('0.00'))
    
    def get_shipping_summary(self):
        # Children must implement this
        # Name, Delivery, Cost
        return (None, None, Decimal('0.00'))
        
    def get_total(self):
        """calculate total"""
        grandtotal = self.get_grandtotal()
        discount = self.get_discount_summary()[1]
        shipping = self.get_shipping_summary()[2]
        #return round(sum([grandtotal, discount, shipping]),2)
        total = round(sum([grandtotal, discount, shipping]),2)
        return Decimal(str(total))


class Item(models.Model):
    """Alias of `Product` stored in collection"""
    qty = models.IntegerField(default=1)
    options = models.ManyToManyField('itemoption', verbose_name=_("options"), blank=True)
    product = GenericForeignKey('content_type', 'object_id')
    unit_price = models.DecimalField(_('sale price'), max_digits=16, 
        decimal_places=4)
    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField(max_length=255)

    class Meta:
        verbose_name = "item"
        verbose_name_plural = "items"
        app_label = 'shop'
        abstract = True

    def __unicode__(self):
        return unicode(self.product)

    def save(self,*args, **kwargs):
        if not self.unit_price:
            self.unit_price = Decimal(str(self.product.get_price()))
        super(Item, self).save(*args, **kwargs)

    def get_price(self):
        """docstring for get_price"""
        item_options = self.options.all()
        price_adjustment = sum([o.price_adjustment for o in item_options])
        return Decimal(self.unit_price + price_adjustment)

    def get_subtotal(self):
        """docstring for get_subtotal"""
        return (self.get_price() * self.qty)

    def get_extended_price(self):
        """Extended price of an item"""
        return self.get_subtotal()

    def get_tax_summary(self, _tax_zone):
        assert _tax_zone is not None
        assert isinstance(_tax_zone, AdminArea)
        
#import pdb
#        pdb.set_trace()

        try:
            applicable_taxes = _tax_zone.tax_rates.all().filter(tax_class__in=self.product.tax.all()).order_by('-tax_class__ordering')
        except:
            return []
                
        applicable_non_stacked_taxes = applicable_taxes.filter(is_stacked=False)
        applicable_stacked_taxes = applicable_taxes.filter(is_stacked=True)

        '''
        non_stacked_taxes = [(t.__unicode__(), t.get_amount(self.get_extended_price())) \
            for t in applicable_non_stacked_taxes]
        '''
        
        non_stacked_taxes = []
        for tax in applicable_non_stacked_taxes:
            if tax.is_per_item:
                non_stacked_taxes.append((tax.__unicode__(), 
                    #tax.get_amount(self.get_extended_price())*self.qty
                    tax.get_amount(self.get_price())*self.qty
                ))
            else:
                non_stacked_taxes.append((tax.__unicode__(), 
                    tax.get_amount(self.get_price())))
        
        price_plus_tax = [tax[1] for tax in non_stacked_taxes]
        price_plus_tax.append(self.get_extended_price())
        price_plus_tax = sum(price_plus_tax)
        
        # Stacked taxes can't be per item based.
        stacked_taxes = [(t.__unicode__(), t.get_amount(price_plus_tax)) \
            for t in applicable_stacked_taxes]
        
        return non_stacked_taxes + stacked_taxes

    def get_tax(self, _tax_zone):
        assert _tax_zone is not None
        assert isinstance(_tax_zone, AdminArea)
        
        tax_summary = self.get_tax_summary(_tax_zone)
        applicable_taxes = [val for key, val in tax_summary]
        return sum(applicable_taxes)

class ItemOption(models.Model):
    name = models.CharField(_('option name'), max_length=255)
    value = models.CharField(_('option value'), max_length=255)
    price_adjustment = models.DecimalField(_("price adjustment"), max_digits=16, 
        decimal_places=4, default='0.00')
    
    class Meta:
        verbose_name = _('item option')
        verbose_name_plural = _('item options')
        app_label = 'shop'
        
    def __unicode__(self):
        return "%s - %s" % (self.name, self.value)

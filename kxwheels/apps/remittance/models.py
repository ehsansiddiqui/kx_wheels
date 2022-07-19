import uuid
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from . import signals as remittance_signals

TRANSACTION_TYPES = {
    'P': 'purchase',
    'PA': 'preauth',
    'PAC': 'capture',
    'R': 'refund',
    'VP': 'void',
    'VR': 'refund',
}

class Request(object):
    def __init__(self, *args, **kwargs):
        # Since it is difficult to guess the attributes required
        # for each gateway, I am keeping this empty for the child 
        # classes to set the attributes dynamically.
        pass
        
    def __repr__(self):
        return u"<A Humble Request>"
        
    def __str__(self):
        return self.__repr__()

    def __unicode__(self):
        return self.__repr__()

class Response(object):
    def __init__(self, *args, **kwargs):
        _date_format = "%Y-%m-%d"
        
        self.purchase = kwargs.get('purchase', '')
        
        self.trans_id = kwargs.get('trans_id','')
        self.trans_type = kwargs.get('trans_type', '')
        self.trans_datetime = kwargs.get('trans_datetime', '')

        self.method = kwargs.get('method','')
        self.gateway = kwargs.get('gateway','')
        self.amount = kwargs.get('amount','')

        self.auth_code = kwargs.get('auth_code','') 
        self.iso_code = kwargs.get('iso_code','')
        self.response_code = kwargs.get('response_code','')
        self.reason_code = kwargs.get('reason_code','')
        
        self.message_id = kwargs.get('message_id', '')
        self.message = kwargs.get('message','')
        self.is_success = kwargs.get('is_success','')
        self.raw = kwargs.get('raw', '')

        self.paypal_email = kwargs.get('paypal_email', '')
       
    def __repr__(self):
        return u"<Response: %s - %s>" % (self.method, self.amount)

    def __str__(self):
        return self.__repr__()

    def __unicode__(self):
        return self.__repr__()
    
    def save(self):
        transaction = self.convert_to_transaction()
        remittance_signals.transaction_complete.send(
            sender=Transaction, 
            instance=transaction
        )
        return transaction
        
    def convert_to_transaction(self):
        fields = [f.name for f in Transaction._meta.fields]
        try:
            trans = Transaction.objects.get(
                purchase=Purchase.objects.get(order=self.purchase),
                trans_id=self.trans_id,
                trans_type=self.trans_type,
            )
        except Transaction.DoesNotExist:
            trans = Transaction(
                purchase=Purchase.objects.get(order=self.purchase),
                trans_id=self.trans_id,
                trans_type=self.trans_type,
            )

        fields.remove('purchase')
        for f in fields:
            try:
                setattr(trans, f, getattr(self, f))
            except AttributeError:
                pass
        trans.save()
        return trans

#---------------------------#
# Persistent storage models #
#---------------------------#

class Seller(models.Model):
    first_name = models.CharField(_('first name'), max_length=255)
    last_name = models.CharField(_('last name'), max_length=255)
    company_name = models.CharField(_('company name'), max_length=255)
    address_1 = models.CharField(_('address line 1'), max_length=255)
    address_2 = models.CharField(_('address line 2'), max_length=255, null=True)
    city = models.CharField(_('city'), max_length=255)
    province = models.CharField(_('province'), max_length=255)
    postal_code = models.CharField(_('postal code'), max_length=255)
    country = models.CharField(_('country'), max_length=255)
    email = models.EmailField(_('email'), max_length=255)
    phone = models.CharField(_('phone'), max_length=255)
    fax = models.CharField(_('fax'), max_length=255)

    def __repr__(self):
        return u"<Seller: %s>" % self.company_name

    def __str__(self):
        return self.__repr__()

    def __unicode__(self):
        return self.__repr__()
        
    def save(self, *args, **kwargs):
        if not self.pk:
            pass
        super(Seller, self).save(*args, **kwargs)
        
    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)
    
class Buyer(models.Model):
    customer = models.ForeignKey(User, verbose_name=_('customer'))
    email = models.EmailField(_('email'), max_length=255)
    
    billing_first_name = models.CharField(_('billing first name'), max_length=255)
    billing_last_name = models.CharField(_('billing last name'), max_length=255)
    billing_company_name = models.CharField(_('billing company name'), max_length=255)
    billing_address_1 = models.CharField(_('billing address line 1'), max_length=255)
    billing_address_2 = models.CharField(_('billing address line 2'), max_length=255)
    billing_city = models.CharField(_('billing city'), max_length=255)
    billing_province = models.CharField(_('billing province'), max_length=255)
    billing_postal_code = models.CharField(_('billing postal code'), max_length=255)
    billing_country = models.CharField(_('billing country'), max_length=255)
    billing_email = models.EmailField(_('billing email'), max_length=255)
    billing_phone = models.CharField(_('billing phone'), max_length=255)
    billing_fax = models.CharField(_('billing fax'), max_length=255)
    
    is_shipping_same_billing = models.BooleanField(_('is_shipping_same_billing'), default=True)
    
    shipping_first_name = models.CharField(_('shipping first name'), max_length=255)
    shipping_last_name = models.CharField(_('shipping last name'), max_length=255)
    shipping_company_name = models.CharField(_('shipping company name'), max_length=255)
    shipping_address_1 = models.CharField(_('shipping address line 1'), max_length=255)
    shipping_address_2 = models.CharField(_('shipping address line 2'), max_length=255)
    shipping_city = models.CharField(_('shipping city'), max_length=255)
    shipping_province = models.CharField(_('shipping province'), max_length=255)
    shipping_postal_code = models.CharField(_('shipping postal code'), max_length=255)
    shipping_country = models.CharField(_('shipping country'), max_length=255)
    shipping_email = models.EmailField(_('shipping email'), max_length=255)
    shipping_phone = models.CharField(_('shipping phone'), max_length=255)
    shipping_fax = models.CharField(_('shipping fax'), max_length=255)
    
    def __repr__(self):
        return u"<Buyer: %s>" % self.billing_full_name

    def __str__(self):
        return self.__repr__()

    def __unicode__(self):
        return self.__repr__()
        
    class Meta:
        verbose_name = _('buyer')
        verbose_name_plural = _('buyers')
        app_label = 'remittance'

    def save(self, *args, **kwargs):
        fields = [ 'first_name', 'last_name', 'company_name', 'address_1', 'address_2', 
        'city', 'province', 'postal_code', 'country', 'phone', 'fax',]
        
        if self.is_shipping_same_billing:
            for field in fields:
                setattr(self, 'shipping_%s' % field, getattr(self, 'billing_%s' % field))
        
        super(Buyer, self).save(*args, **kwargs)
    
    @property
    def billing_full_name(self):
        return "%s %s" % (self.billing_first_name, self.billing_last_name)
    
    @property
    def shipping_full_name(self):
        return "%s %s" % (self.shipping_first_name, self.shipping_last_name)


class Purchase(models.Model):
    slug = models.CharField(max_length=32, unique=True, blank=True)
    order = models.CharField(_('order number'), max_length=255,)
    seller = models.ForeignKey('Seller', verbose_name=_('seller'),
        related_name='purchases')
    buyer = models.ForeignKey('Buyer', verbose_name=_('buyer'), 
        related_name='purchases')
    subtotal = models.DecimalField(_("subtotal"), max_digits=16, 
        decimal_places=2, blank=True, null=True)
    tax = models.DecimalField(_("tax"), max_digits=16, 
        decimal_places=2, blank=True, null=True)
    shipping = models.DecimalField(_("shipping & handling"), max_digits=16, 
        decimal_places=2, blank=True, null=True)
    discount = models.DecimalField(_("discount"), max_digits=16, 
        decimal_places=2, blank=True, null=True)
    total = models.DecimalField(_("total"), max_digits=16, 
        decimal_places=2, blank=True, null=True)
    currency = models.CharField(_("ISO currency code"), max_length=3,)
    note = models.TextField(_('purchase note'), blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = uuid.uuid4().hex
        super(Purchase, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('remittance_purchase_detail', [self.slug])

    class Meta:
        verbose_name = _("purchase")
        verbose_name_plural = _("purchases")
        app_label = 'remittance'
        
    def get_balance(self):
        transactions = self.transactions.filter(is_success=True)
        trans_amount = sum([t.amount for t in transactions])
        return Decimal(self.total) - trans_amount
        

class PurchaseItem(models.Model):
    purchase = models.ForeignKey('Purchase', verbose_name=_('purchase'), 
        related_name='items')
    sku = models.CharField(_('sku'), max_length=255)
    name = models.CharField(_('name'), max_length=255)
    desc = models.TextField(_('desc'), max_length=255, null=True,)
    qty = models.IntegerField(_('qty'))
    unit_price = models.DecimalField(_("unit price"), max_digits=16, 
        decimal_places=2, blank=True, null=True)
    discount = models.DecimalField(_("discount"), max_digits=16, 
        decimal_places=2, blank=True, null=True, default='-0.00')
    ext_price = models.DecimalField(_("extended price"), max_digits=16, 
        decimal_places=2, blank=True, null=True,)
    tax = models.DecimalField(_("tax"), max_digits=16, 
        decimal_places=2, blank=True, null=True)
            
    def __unicode__(self):
        return '%s: %s' % (self.sku, self.unit_price)

    class Meta:
        verbose_name = _("purchase item")
        verbose_name_plural = _("purchase items")
        app_label = 'remittance'
        
class Transaction(models.Model):
    purchase = models.ForeignKey('Purchase', verbose_name=_('Purchase'), 
        related_name='transactions')
    trans_id = models.CharField(_("Transaction ID"), max_length=45, 
        primary_key=True)
    trans_type = models.CharField(_("Transaction Type"), max_length=45)
    trans_datetime = models.DateTimeField(_("Transaction Datetime"))
    
    amount = models.DecimalField(_("Amount"), max_digits=18, 
        decimal_places=4, default='0.00')
    method = models.CharField(_("Method"), max_length=255)
    gateway = models.CharField(_("Gateway"), max_length=255)
    
    auth_code = models.CharField(_("Auth Code"), max_length=255) 
    iso_code = models.CharField(_("ISO Code"), max_length=255)
    response_code = models.CharField(_("Response Code"), max_length=255)
    reason_code = models.CharField(_('Reason Code'),  max_length=255)

    message = models.CharField(_("Message"), max_length=255)
    is_success = models.BooleanField(_('Approved?'), default=False)
    raw = models.TextField(_('Raw'))
    
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    
    paypal_email = models.CharField(_("paypal_email"),null=True,blank=True, max_length=255)

    def __unicode__(self):
        if self.pk is not None:
            return u"%s" % self.pk
        else:
            return u"Transaction (unsaved)"

    class Meta:
        verbose_name = _("transaction")
        verbose_name_plural = _("transactions")
        app_label = 'remittance'
        

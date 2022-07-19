from django.db import models
from datetime import datetime
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from kxwheels.apps.shop.models import Option
from kxwheels.apps.shop.utils import slugify
from kxwheels.apps.shop.templatetags import shop_filters

class BaseProductManager(models.Manager):
    def active(self, **kwargs):
        return self.filter(is_active=True, **kwargs)
        
    def get_by_sku(self, sku, **kwargs):
        return self.get(sku=sku, **kwargs)

class BaseProduct(models.Model):
    """
    If the extending models need to assign products to categories, use the following
    category = models.ManyToManyField(Category, blank=True, verbose_name=_("category"))
    """
    site = models.ForeignKey(Site, verbose_name=_("site"), blank=True,)
    sku = models.CharField(_("SKU"), max_length=255, blank=True, null=True, unique=True)
    name = models.CharField(_("name"), max_length=255,)
    slug = models.SlugField(_("slug"), max_length=255, 
        help_text=_("Leave blank to auto-generate"), blank=True)
    short_desc = models.CharField(_("short description"), max_length=255, blank=True, null=True) 
    long_desc = models.TextField(_("long description"), blank=True, null=True)
    quantity = models.IntegerField(_("quantity"), default=1, help_text=_('in stock'))
    cost = models.DecimalField(_("cost"), max_digits=16, decimal_places=4, blank=True, null=True)    
    price = models.DecimalField(_("price"), max_digits=16, decimal_places=4)

    special_price = models.DecimalField(_("special price"), max_digits=16, 
        decimal_places=4, blank=True, null=True)
    spvf = models.DateTimeField(_("special price valid from"), blank=True, null=True)
    spvt = models.DateTimeField(_("special price valid till"), blank=True, null=True)

    options = models.ManyToManyField('option', verbose_name=_("Options"), blank=True)
    tax = models.ManyToManyField('TaxClass', verbose_name=_("tax"), blank=True)
    
    meta_title = models.CharField(_('meta title'), max_length=255, blank=True, null=True)
    meta_keywords = models.CharField(_('meta keywords'), max_length=255, blank=True, null=True)
    meta_description = models.CharField(_('meta description'), max_length=500, blank=True, null=True) 
    
    is_active = models.BooleanField(_("is active?"), default=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True, blank=True)
    real_type = models.ForeignKey(ContentType, editable=False, null=True)

    objects = BaseProductManager()
    
    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products" 
        app_label = 'shop'
        abstract = True

    def save(self, *args, **kwargs):
        self.real_type = self._get_real_type()
        if not self.slug:
            self.slug = slugify(self.name, instance=self)            
        super(BaseProduct, self).save(*args, **kwargs)
    
    def _get_real_type(self):
        return ContentType.objects.get_for_model(type(self))

    def cast(self):
        return self.real_type.get_object_for_this_type(pk=self.pk)
    
    def get_price(self):
        if self.special_price and (self.spvf or self.spvt):
            return self.special_price
        else:
            return self.price
            
    def get_price_display(self):
        if self.special_price and (self.spvf or self.spvt):
            return '''<del>%s</del> %s''' % (
                shop_filters.currency(self.price), 
                shop_filters.currency(self.special_price)
            )
        else:
            return '%s' % shop_filters.currency(self.price)
    
class HardProduct(BaseProduct):
    """
    Defines non-digital products that are shippable.
    """
    weight = models.DecimalField(_("weight"), max_digits=8, 
        decimal_places=2, blank=True, null=True)
    weight_unit = models.CharField(_('weight unit'), max_length="50",
        default='kg',)
    length = models.DecimalField(_("length"), max_digits=8, 
        decimal_places=2, blank=True, null=True)
    length_unit = models.CharField(_('length unit'), max_length="50",
        default='m',)
    width = models.DecimalField(_("width"), max_digits=8, 
        decimal_places=2, blank=True, null=True)
    width_unit = models.CharField(_('width unit'), max_length="50",
        default='m',)
    height = models.DecimalField(_("height"), max_digits=8, 
        decimal_places=2, blank=True, null=True)
    height_unit = models.CharField(_('height unit'), max_length="50",
        default='m',)

    """
    @models.permalink
    def get_absolute_url(self):
        return ('shop.views.product', [self.pk])
    """
    
    def save(self, *args, **kwargs):
        """docstring for save"""
        self.site = Site.objects.get_current()
        super(HardProduct, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name = "hard product"
        verbose_name_plural = "hard products" 
        abstract = True
        app_label = 'shop'

class SoftProduct(BaseProduct):
    """
    Defines digital products that are downloadable
    """
    attachment = models.FileField(upload_to='softproducts', blank=True, null=True)
    download_tries = models.IntegerField(_("download tries"), blank=True, null=True )
    link_expiry = models.IntegerField(_("link expiry"), help_text=_("in hours"),
        blank=True, null=True)
    is_downloadable = models.BooleanField(_("is the product downloadable?"))

    def save(self, *args, **kwargs):
        """docstring for save"""
        self.site = Site.objects.get_current()
        super(SoftProduct, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "soft product"
        verbose_name_plural = "soft products" 
        abstract = True
        app_label = 'shop'

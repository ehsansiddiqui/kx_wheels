from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel
from kxwheels.apps.shop.utils import slugify

class ProductCategory(MPTTModel):
    site = models.ForeignKey(Site, verbose_name=_("site"), blank=True, 
        related_name="shop_category")
    name = models.CharField(_("name"), max_length=200)
    slug = models.SlugField(_("slug"), max_length=255, 
        help_text=_("Leave blank to auto-generate"), blank=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='child')
    meta = models.TextField(_("meta description"), blank=True, null=True,)
    description = models.TextField(_("description"), blank=True, help_text="Optional")
    ordering = models.IntegerField(_("ordering"), default=0,)
    is_active = models.BooleanField(_("is active?"), default=True, blank=True)
    related_categories = models.ManyToManyField('self', blank=True, null=True,
        verbose_name=_('Related Categories'), related_name='related_categories')
        
    class Meta:
        abstract = True
        ordering=('ordering',)
        app_label = 'shop'

    class MPTTMeta:
        order_insertion_by=['ordering',]
        
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, instance=self)
        super(ProductCategory, self).save(*args, **kwargs)
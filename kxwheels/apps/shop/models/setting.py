from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from kxwheels.apps.l10n.models import (AdminArea,)

class SettingManager(models.Manager):
    def get_current(self):
        """return current site configuration based on current site"""
        try:
            setting = self.get(site=Site.objects.get_current())
            return setting
        except Setting.DoesNotExist:
            raise Exception("Please configure the shop before using it.")

class Setting(models.Model):
    """
    Used to store specific information about a store. Also used to
    configure various store behaviours.
    """
    site = models.OneToOneField(Site, verbose_name=_("site"), 
        primary_key=True, blank=True, related_name="shop_setting")
    store_name = models.CharField(_("store name"), max_length=100, unique=True)
    store_description = models.TextField(_("description"), blank=True, null=True)
    store_email = models.EmailField(_("store email"),)
    store_orders_email = models.EmailField(_("orders email"),)
    street1 = models.CharField(_("st. address 1"),max_length=255,)
    street2 = models.CharField(_("st. address 2"), max_length=50, blank=True, null=True)
    city = models.CharField(_("city"), max_length=255,)
    province = models.CharField(_("province"), max_length=255)
    postal_code = models.CharField(_("postal code"), max_length=20)
    country = models.CharField(_("country"), max_length=255)
    phone = models.CharField(_("phone number"), max_length=30)
    fax = models.CharField(_("fax number"), max_length=30)

    objects = SettingManager()
    
    class Meta:
        verbose_name = "setting"
        verbose_name_plural = "settings"
        app_label = 'shop'
    
    def __unicode__(self):
        return u'%s - %s' % (self.site.name, self.store_name)
        
    def save(self, *args, **kwargs):
        self.site = Site.objects.get_current()
        super(Setting, self).save(*args, **kwargs)
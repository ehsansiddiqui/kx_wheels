from django.db import models
from django.utils.translation import ugettext_lazy as _

OPTION_TYPES = (
    (0, 'Text Input'),
    (1, 'Select Input')
)

class Option(models.Model):
    """ Like color, size, packaging etc"""
    name = models.CharField(max_length=255,)
    type = models.IntegerField(_('option type'), choices=OPTION_TYPES, 
        default=1, help_text=_('Product options will be ignored when using Text Input'))
    ordering = models.IntegerField(_("sort order"), default=0)
    
    class Meta:
        app_label = 'shop'
        
    def __unicode__(self):
      return self.name

class ProductOption(models.Model):
    """ X tshirt has option set color. customer would choose the option"""
    option = models.ForeignKey(Option, related_name="product_options")
    value = models.CharField(_("value"), max_length=100,)
    price_adjustment = models.DecimalField(_("price adjustment"), max_digits=16, 
        decimal_places=4, help_text=_("enter either negetive or postive value"),
        default='0.00')
    ordering = models.IntegerField(_("sort order"), default=0)
    
    class Meta:
        app_label = 'shop'
        
    def __unicode__(self):
        return "%s - %s" % (self.option.name, self.value)
from decimal import Decimal
from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from kxwheels.apps.l10n.models import AdminArea

class TaxClass(models.Model):
    """Holds taxes information."""
    site = models.ForeignKey(Site, verbose_name=_("site"),
        related_name="taxclasses")
    name = models.CharField(_("name"), max_length=100)
    number = models.CharField(_("registration number"), max_length=100, 
        blank=True, null=True)
    description = models.TextField(_("description"))
    default_rate = models.DecimalField(_("default rate"), max_digits=4, 
        decimal_places=2,help_text = _("Default rate will be used if tax rate \
        is not defined"),
    )
    ordering = models.IntegerField(_("order"), default=0, help_text=_('order \
        in which this tax is applied'))

    def __unicode__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = "tax class"
        verbose_name_plural = "tax classes"
        app_label = 'shop'

class TaxRate(models.Model):
    """Contains different tax rates to be used"""
    KIND_CHOICES = (
        ('amount', 'Amount'),
        ('percentage', 'Percentage'),
    )
    
    tax_class = models.ForeignKey(TaxClass, related_name="rates")
    tax_zone = models.ForeignKey(AdminArea, blank=True, null=True, 
        verbose_name='tax zone', related_name="tax_rates")
    kind = models.CharField(choices=KIND_CHOICES, max_length=15, default='percentage')
    value = models.DecimalField(_("value"), max_digits=16, decimal_places=4)
    is_stacked = models.BooleanField(_('is stacked?'), default=0)
    is_per_item = models.BooleanField(_('is per item?'), default=0)
    
    class Meta:
        verbose_name = "tax rate"
        verbose_name_plural = 'tax rates'
        app_label = 'shop'
        unique_together = ('tax_class', 'tax_zone',)

    def __unicode__(self):
        if self.kind == self.KIND_CHOICES[0][0]:
            value="$%s" % self.value 
        elif self.kind == self.KIND_CHOICES[1][0]:
            value="%s%%" % self.value

        if self.tax_class.number:
            return '%s [%s] @ %s' % (
                self.tax_class.name, 
                self.tax_class.number, 
                value
            )
        else:
            return '%s @ %s' % (self.tax_class.name, value)

    def get_amount(self, subtotal):
        """docstring for get_discount_amount"""
        if self.kind == self.KIND_CHOICES[0][0]:
            amount =  Decimal(self.value)
        elif self.kind == self.KIND_CHOICES[1][0]:
            amount = Decimal(subtotal * (self.value/100))
        return amount
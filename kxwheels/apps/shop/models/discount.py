from decimal import Decimal
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Discount(models.Model):
    KIND_CHOICES = (
        ('amount', 'Discount amount'),
        ('percentage', 'Discount percentage'),
    )
    
    code = models.CharField(_('discount code'), max_length=255, primary_key=True)
    kind = models.CharField(choices=KIND_CHOICES, max_length=15, default='percentage')
    value = models.DecimalField(_("value"), max_digits=16, decimal_places=4)  
    short_desc = models.CharField(_("short description"), max_length=100)
    long_desc = models.TextField(_("long description"), blank=True, null=True)
    valid_from = models.DateTimeField(_("valid from"), blank=True, null=True)
    valid_till = models.DateTimeField(_("valid till"), blank=True, null=True)
    is_active = models.BooleanField(_("is active?"), default=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    
    class Meta:
        app_label = 'shop'
        
    def clean(self):
        from django.core.exceptions import ValidationError
        # Check for percentage value
        if self.kind == 'percentage' and (self.value > 100 or self.value < 0):
            raise ValidationError('The value must be between 0 and 100 when using percentage.')
       
    def __unicode__(self):
        """docstring for __unicode__"""
        return self.code

    def get_amount(self, subtotal):
        """docstring for get_discount_amount"""
        if self.kind == 'amount':
            amount =  Decimal(self.value * -1)
        elif self.kind == 'percentage':
            amount = Decimal(subtotal * (self.value/100) * -1)
        return amount
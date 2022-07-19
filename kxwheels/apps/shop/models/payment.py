from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from kxwheels.apps.shop.models import Order

TRANSACTION_TYPES = (
    ('purchase', 'Purchase'),
    ('preauth', 'PreAuth'),
    ('capture', 'Capture'),
    ('void', 'Void'),
    ('refund', 'Refund'),
)

class Payment(models.Model):
    trans_id = models.CharField(_("Transaction ID"), max_length=45, primary_key=True)
    trans_type = models.CharField(_("Transaction Type"), choices=TRANSACTION_TYPES, max_length=45)
    trans_datetime = models.DateTimeField(_("Transaction Datetime"))
    order = models.ForeignKey(Order, verbose_name=_('Order'), related_name='payments')
    amount = models.DecimalField(_("Amount"), max_digits=18, decimal_places=4, default='0.00')
    method = models.CharField(_("Method"), max_length=25)
    gateway = models.CharField(_("Gateway"), max_length=25)
    
    auth_code = models.CharField(_("Auth Code"), max_length=255) 
    iso_code = models.CharField(_("ISO Code"), max_length=255)
    response_code = models.CharField(_("Response Code"), max_length=255)
    reason_code = models.CharField(_('Reason Code'),  max_length=255)

    message = models.CharField(_("Message"), max_length=255)
    is_success = models.BooleanField(_('Approved?'), default=False)
    raw = models.TextField(_('Raw'))
    
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def __unicode__(self):
        if self.pk is not None:
            return u"%s" % self.pk
        else:
            return u"Payment (unsaved)"

    class Meta:
        verbose_name = _("payment")
        verbose_name_plural = _("payments")
        app_label = 'shop'
        
        
    def is_complete(self):
        completions = Payment.objects.filter(trans_type != 'preauth')
        if completions:
            return True
        else:
            return False

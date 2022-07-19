from django import forms
from django.utils import importlib
from django.utils.translation import ugettext_lazy as _
from . import get_module

PaymentForm = getattr(get_module(), 'PaymentForm')
        
class PayPalForm(forms.Form):
    notes = forms.EmailField(label=_('Enter your email if you want to pay via paypal.'), widget=forms.Textarea, required=False)

class CaptureForm(forms.Form):
    order_id = forms.CharField(label=_('Order ID'), max_length=255)
    trans_id = forms.CharField(label=_('Transaction ID'), max_length=255)
    amount = forms.CharField(label=_('Amount'), max_length=255)
    
        
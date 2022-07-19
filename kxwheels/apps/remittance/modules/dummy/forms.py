from datetime import datetime
from django import forms
from django.utils.translation import ugettext_lazy as _
from kxwheels.apps.remittance.utils import is_valid_cc

class PaymentForm(forms.Form):
    now = datetime.now()
    MONTHS = (
        ('01', '01 - Jan'),
        ('02', '02 - Feb'),
        ('03', '03 - Mar'),
        ('04', '04 - Apr'),
        ('05', '05 - May'),
        ('06', '06 - Jun'),
        ('07', '07 - Jul'),
        ('08', '08 - Aug'),
        ('09', '09 - Sep'),
        ('10', '10 - Oct'),
        ('11', '11 - Nov'),
        ('12', '12 - Dec'),
    )

    YEARS = [(str(i)[2:], i) for i in range(now.year, now.year+8)]
    
    CARD_TYPES = (
        ('Visa', 'Visa',),
        ('Master Card', 'Master Card'),
        ('Amex', 'American Express'),
        ('Diners Club', 'Diners Club'),
        ('Discover', 'Disover'),
    )

    name = forms.CharField(label=_('Name as on card'),  max_length=255,
                           help_text=_("Exactly as displayed on the card"))
    type = forms.ChoiceField(label=_('Card Type'), choices=CARD_TYPES)
    number = forms.CharField(label=_('Card Number'), max_length=16)
    exp_month = forms.ChoiceField(label=_('Expiry month'), choices=MONTHS, 
        initial="%02d" % now.month)
    exp_year = forms.ChoiceField(label=_('Expiry year'), choices=YEARS)
    cvd = forms.CharField(label=_('CVD / CVV'), max_length=5)

    def clean(self):
        cleaned_data = self.cleaned_data
        month = int(cleaned_data['exp_month'])
        year = cleaned_data['exp_year']
        if year == str(self.now.year)[2:] and month < self.now.month:
            raise forms.ValidationError("You credit card seems to have expired.")
        return cleaned_data

    def clean_number(self):
        number = self.cleaned_data.get('number')
        if not is_valid_cc(number):
            raise forms.ValidationError("Credit card number you entered seems to be invalid.")
        return number

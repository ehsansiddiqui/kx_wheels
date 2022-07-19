import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from registration.forms import RegistrationFormTermsOfService as RFTOS, RegistrationForm
from registration.forms import RegistrationFormUniqueEmail as RFUE

from kxwheels.apps.account.models import Profile, Dealer
from kxwheels.apps.kx.models.tire import TireManufacturer, TireManufacturerDiscount
from kxwheels.apps.kx.models.wheel import WheelManufacturer, WheelManufacturerDiscount
from kxwheels.apps.l10n.forms import AddressForm


# Customized version of http://djangosnippets.org/snippets/686/
class RegistrationFormNoUserName(RFUE, RFTOS):
    """
    A registration form that only requires the user to enter their e-mail 
    address and password. The username is automatically generated
    This class requires django-registration to extend the 
    RegistrationFormUniqueEmail
    """
    # def __init__(self,*args,**kwargs):
    #     super(RegistrationFormNoUserName, self).__init__(*args, **kwargs)
    #     self.fields.insert(-1,'tos', self.fields.pop('tos'))
    #     self.fields.insert(-1,'last_name', self.fields.pop('last_name'))

    username = forms.CharField(widget=forms.HiddenInput, required=False)
    first_name = forms.CharField(label=_('First name'), max_length=255, required=True)
    last_name = forms.CharField(label=_('Last name'), max_length=255, required=True)

    def clean_username(self):
        "This function is required to overwrite an inherited username clean"
        return self.cleaned_data['username']

    def clean(self):
        if not self.errors:
            self.cleaned_data['username'] = '%s%s' % (self.cleaned_data['email'].split('@',1)[0], User.objects.count())
        super(RegistrationFormNoUserName, self).clean()
        return self.cleaned_data


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'site', 'name', 'subdomain', 'dealer_lolast_go', 'banner')

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        # Pull the fields from AddressForm in l10n app
        for key, value in AddressForm.base_fields.items():
            self.fields[key] = value
    def save(self, *args, **kwargs):
        instance = super(ProfileForm, self).save(*args, **kwargs)
        if instance.subdomain:
            # Add the default discounts.
            if not WheelManufacturerDiscount.objects.filter(user=instance.user).count():
                for manufacturer in WheelManufacturer.objects.all():
                    mark = WheelManufacturerDiscount.objects.create(
                        user=instance.user,
                        manufacturer=manufacturer,
                        is_visible=True,
                        discount=13,
                    )
                    mark.save()
            if not TireManufacturerDiscount.objects.filter(user=instance.user).count():
                for manufacturer in TireManufacturer.objects.all():
                    mark = TireManufacturerDiscount.objects.create(
                        user=instance.user,
                        manufacturer=manufacturer,
                        is_visible=True,
                        discount=13,
                    )
                    mark.save()
        return instance
        
    def get_digits(self, string):
        return

    def clean_name(self):
        """docstring for clean"""
        _user = self.instance.user
        _name = re.sub(r'[^0-9a-zA-Z-_]+', '-', self.cleaned_data.get('name'))
        _err_msg = "You have another profile named '%s'. Please choose another name." % _name

        if self.instance.pk is not None:
            if Profile.objects.filter(name=_name, user=_user).exclude(pk=self.instance.pk).exists():
                raise ValidationError(_err_msg)
        else:
            if Profile.objects.filter(name=_name, user=_user).exists():
                raise ValidationError(_err_msg)
        return _name

    def clean_landline_phone(self):
        landline_phone = self.cleaned_data.get('landline_phone')
        landline_phone = ''.join([s for s in list(landline_phone) if s.isdigit()])
        return landline_phone

    def clean_cell_phone(self):
        cell_phone = self.cleaned_data.get('cell_phone')
        cell_phone = ''.join([s for s in list(cell_phone) if s.isdigit()])
        return cell_phone

    def clean_fax(self):
        fax = self.cleaned_data.get('fax')
        fax = ''.join([s for s in list(fax) if s.isdigit()])
        return fax

    def clean_subdomain(self):
        subdomain = self.cleaned_data.get('subdomain')
        if not subdomain:
            return None
        return subdomain

    # The code below is copied from AddressForm in l10n App
    def clean_postal_code(self):
        _postal_code = self.cleaned_data.get('postal_code').upper()
        _postal_code = _postal_code.replace(' ', '')
        return _postal_code

class ProfileAdminForm(ProfileForm):
    class Meta:
        exclude=('user','site','name')
        model=Profile

class DealerForm(forms.ModelForm):

    business_kind = forms.ChoiceField(label=_("What kind of business do you have?"),
        choices=Dealer.BUSINESS_KINDS,
        widget=forms.RadioSelect)

    class Meta:
        model = Dealer
        exclude = []
from django import forms
from django.utils.translation import ugettext_lazy as _

from kxwheels.apps.l10n.models import AdminArea, Country


class AddressForm(forms.Form):

    admin_areas = [(i['pk'], i['name']) for i in AdminArea.objects.values('pk', 'name')]
    countries = [(i['pk'], i['name']) for i in Country.objects.values('pk', 'name')]
    admin_areas.insert(0, ('','---------'))
    countries.insert(0, ('','---------'))

    first_name = forms.CharField(label=_('first name'), max_length=100)
    last_name = forms.CharField(label=_('last name'), max_length=100)
    address_1 = forms.CharField(label=_('address line 1'), max_length=100)
    address_2 = forms.CharField(label=_('address line 2'), max_length=100, required=False)
    city = forms.CharField(label=_('city'), max_length=100)
    province = forms.ChoiceField(label=_('province/state'), choices=admin_areas)
    postal_code = forms.CharField(label=_('postal/zip code'), max_length=50)
    country = forms.ChoiceField(label=_('country'), choices=countries)

    landline_phone = forms.CharField(label=_('landline phone'), max_length=16)
    cell_phone = forms.CharField(label=_('cell phone'), max_length=16, required=False)
    fax = forms.CharField(label=_('fax'), max_length=16, required=False)

    def clean_postal_code(self):
        postal_code = self.cleaned_data.get('postal_code').upper()
        postal_code = postal_code.replace(' ', '')

        '''
        if not re.search(r"([A-Z]{1}[0-9]{1}){3}", _postal_code):
            self._errors["postal_code"] = ErrorList([_("Postal code \
            must be in the format: A0A0A0")])
        '''
        return postal_code

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

import datetime

from django import forms
from django.contrib.contenttypes.models import ContentType
from django.forms.formsets import BaseFormSet
from django.utils.translation import ugettext_lazy as _

from kxwheels.apps.remittance.models import Purchase, Transaction
from kxwheels.apps.shop.models import (TaxRate, CartItem, Order, OrderNote, Discount,
                                       )
from kxwheels.apps.shop.utils import is_valid_cc, is_valid_generic_object


class BaseAddressFormSet(BaseFormSet):
    # make = forms.CharField(label=_('Make'), max_length=16)
    def clean(self):
        if any(self.errors):
            return
        for i in range(0, self.total_form_count()):
            form = self.forms[i]
            if not form.has_changed() and not form.is_valid():
                raise forms.ValidationError("Please make sure you fill both the addresses.")

class CCForm(forms.Form):
    
    now = datetime.datetime.now()
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
    
    name = forms.CharField(label=_('Name as on card'), max_length=255)
    card_number = forms.CharField(label=_('Card Number'), max_length=16)
    exp_month = forms.ChoiceField(label=_('Expiry month'), choices=MONTHS)
    exp_year = forms.ChoiceField(label=_('Expiry year'), choices=YEARS)
    cvd = forms.CharField(label=_('CVD / CVV'), max_length=5)
    
    def clean(self):
        cleaned_data = self.cleaned_data
        month = int(cleaned_data['exp_month'])
        year = cleaned_data['exp_year']
        if year == str(self.now.year)[2:] and month < self.now.month:
            raise forms.ValidationError("You credit card seems to have expired.")
        return cleaned_data
    
    def clean_card_number(self):
        card_number = self.cleaned_data.get('card_number')
        if not is_valid_cc(card_number):
            raise forms.ValidationError("Credit card number you entered seems to be invalid.")
        return card_number
        
class CaptureForm(forms.Form):
    order_id = forms.CharField(label=_('Order ID'), max_length=255)
    trans_id = forms.CharField(label=_('Transaction ID'), max_length=255)
    amount = forms.CharField(label=_('Amount'), max_length=255)
    
class DiscountCodeForm(forms.Form):
    code = forms.CharField(label=_('Discount code'), max_length=255, required=False)
    
    def clean_code(self):
        code = self.cleaned_data.get('code', None)
        if code:
            try:
                discount = Discount.objects.get(code__iexact=code)
            except Discount.DoesNotExist:
                raise forms.ValidationError('Coupon code you \
                    entered is not valid. Perhaps, it may have expired.')
        return code

class ShippingForm(forms.Form):

    shipping_option = forms.ModelChoiceField(_('Shipping option'))
    
    def __init__(self, *args, **kwargs):
        try:
            cart = kwargs.pop('cart')
        except KeyError:
            cart = None # if normal form
        else:
            super(ShippingForm, self).__init__(*args, **kwargs)
            if cart is not None:
                self.fields['shipping_option'].queryset=cart.shipping_quotes.all()
                self.fields['shipping_option'].empty_label=None


class VehicleForm(forms.Form):
    make = forms.CharField(label=_('Make'), max_length=256)
    year = forms.CharField(label=_('Year'), max_length=256)
    model = forms.CharField(label=_('Model'), max_length=256)

    def __init__(self, *args, **kwargs):
        super(VehicleForm, self).__init__(*args, **kwargs)
        from django.forms.widgets import HiddenInput
        self.fields['make'].widget = HiddenInput()
        self.fields['year'].widget = HiddenInput()
        self.fields['model'].widget = HiddenInput()

class AddToCartForm(forms.Form):
    content_type_id = forms.CharField(max_length=100, widget=forms.HiddenInput())
    object_id = forms.CharField(max_length=100, widget=forms.HiddenInput())
    quantity = forms.CharField(max_length=100, initial=1)
    make  = forms.CharField(max_length=100, initial=1)
    year = forms.CharField(max_length=100, initial=1)

    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product', None)

        # See template_tags for more information about product arg
        super(AddToCartForm, self).__init__(*args, **kwargs)

        if product is not None:
            self.fields['content_type_id'].initial = ContentType.objects.get_for_model(product).pk
            self.fields['object_id'].initial = product.pk

            for option in product.options.all():
                if option.type == 0 :
                    self.fields["option_%s" % option.pk] = forms.CharField(
                        label=option.name, max_length=100)
                elif option.type == 1:
                    _product_options = option.product_options.all()
                    self.fields["option_%s" % option.pk] = forms.ModelChoiceField(
                        label=option.name, queryset=_product_options)

    def clean(self):
        cleaned_data = self.cleaned_data
        content_type_id = cleaned_data.get('content_type_id')
        object_id = cleaned_data.get('object_id')
        if is_valid_generic_object(content_type_id, object_id):
            return cleaned_data
        else:
            raise forms.ValidationError("Could not add product to the cart \
                Invalid product specified.")

class AdminTaxRateForm(forms.ModelForm):
    class Meta:
        model = TaxRate
        exclude = []

    def clean(self):
        """docstring for clean"""
        cleaned_data = self.cleaned_data
        is_stacked = cleaned_data.get('is_stacked')
        is_per_item = cleaned_data.get('is_per_item')
        
        if is_stacked and is_per_item:
            raise forms.ValidationError("You may not select both \
                stacked and per item types. Please choose one.")
                
        return cleaned_data
        
class CartItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        return super(CartItemForm, self).__init__(*args, **kwargs)
    
    class Meta:
        model = CartItem
        exclude = []

class AdminOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('customer_notes', 'items',)

    def get_transactions(self):
        transactions = []
        if self.instance:
            purchases = Purchase.objects.filter(order=self.instance.id)
            for p in purchases:
                transactions.extend(list(Transaction.objects.filter(purchase=p)))
        return transactions
        
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('shipping_option', 'shipping_cost', 'customer', 
            'items', 'status', 'site')
        
class OrderNoteForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        return super(OrderNoteForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        kwargs['commit']=False
        obj = super(OrderNoteForm, self).save(*args, **kwargs)
        if self.request:
            obj.staff = self.request.user
        obj.save()
        return obj

    class Meta:
        model = OrderNote
        exclude = []
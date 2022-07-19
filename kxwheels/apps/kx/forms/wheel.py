from django import forms
from django.db.models import Q
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe

from haystack.query import SearchQuerySet
from haystack.forms import SearchForm

from kxwheels.apps.reviews.forms import BaseReviewForm
from kxwheels.apps.kx.models import (WheelManufacturer, WheelCustomerMedia, WheelSize, WheelReview)
from kxwheels.apps.vehicle.models import (BoltPattern, WheelWidth, Finish)

DIAMETERS = [(i, i) for i in range(13, 31)]
WHEELWIDTHS = [(ww.value, ww.value) for ww in WheelWidth.objects.all().order_by('sort_order')]
BOLTPATTERNS = [(bp.value, bp.value) for bp in BoltPattern.objects.all().order_by('pk')]
FINISHES = [(f.value, f.value) for f in Finish.objects.all().order_by('value')]

DIAMETERS.insert(0, ('','---------'))
WHEELWIDTHS.insert(0, ('','---------'))
BOLTPATTERNS.insert(0, ('','---------'))
FINISHES.insert(0, ('','---------'))

class WheelSizeSearchForm(SearchForm):
    q = forms.CharField(max_length=100, initial='*', widget=forms.HiddenInput())
    diameter = forms.ChoiceField(choices=DIAMETERS, required=False)
    wheelwidth = forms.ChoiceField(choices=WHEELWIDTHS, required=False)
    boltpattern = forms.ChoiceField(choices=BOLTPATTERNS, required=False)
    offset_min = forms.CharField(max_length=5, required=False)
    offset_max = forms.CharField(max_length=5, required=False)

    front_diameter = forms.CharField(required=False, widget=forms.HiddenInput())
    rear_diameter = forms.CharField(required=False, widget=forms.HiddenInput())
    front_wheelwidth = forms.CharField(required=False, widget=forms.HiddenInput())
    rear_wheelwidth = forms.CharField(required=False, widget=forms.HiddenInput())
    front_offset = forms.CharField(max_length=5, required=False, widget=forms.HiddenInput())
    rear_offset = forms.CharField(max_length=5, required=False, widget=forms.HiddenInput())

    finish = forms.ChoiceField(choices=FINISHES, required=False)
    sku = forms.CharField(label="SKU / Part #", max_length=20, required=False)

    manufacturer = forms.ModelChoiceField(
        queryset=WheelManufacturer.objects.visible(),
        required=False, #widget=forms.CheckboxSelectMultiple(),
    )

    availability = forms.MultipleChoiceField(
        choices=WheelSize.AVAILABILITY_CHOICES,
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        #super(WheelSizeSearchForm, self)
        cleaned_data = getattr(self, 'cleaned_data', None)
        sqs = SearchQuerySet().models(WheelSize)

        if cleaned_data is None:
            return sqs

        # SKU
        sku = cleaned_data['sku']
        if sku:
            sqs = sqs.filter(sku=sku)

        # Manufacturer
        manufacturer = cleaned_data['manufacturer']
        if manufacturer:
            sqs = sqs.filter(manufacturer=manufacturer)

        # Diameter
        diameter = cleaned_data['diameter']
        front_diameter = cleaned_data['front_diameter']
        rear_diameter = cleaned_data['rear_diameter']

        if diameter:
            sqs = sqs.filter(diameter=diameter)
        else:
            if front_diameter and not rear_diameter:
                front_diameter = [int(i.strip()) for i in front_diameter.split(',')]
                sqs = sqs.filter(Q(diameter__range=front_diameter))
            elif not front_diameter and rear_diameter:
                rear_diameter = [int(i.strip()) for i in rear_diameter.split(',')]
                sqs = sqs.filter(Q(diameter__range=rear_diameter))
            elif front_diameter and rear_diameter:
                front_diameter = [int(i.strip()) for i in front_diameter.split(',')]
                rear_diameter = [int(i.strip()) for i in rear_diameter.split(',')]
                sqs = sqs.filter(Q(diameter__range=front_diameter) |\
                                 Q(diameter__range=rear_diameter))

        # Wheelwidth
        wheelwidth = cleaned_data['wheelwidth']
        front_wheelwidth = cleaned_data['front_wheelwidth']
        rear_wheelwidth = cleaned_data['rear_wheelwidth']

        if wheelwidth:
            sqs = sqs.filter(wheelwidth=wheelwidth)
        else:
            if front_wheelwidth and not rear_wheelwidth:
                front_wheelwidth = [float(i.strip()) for i in front_wheelwidth.split(',')]
                sqs = sqs.filter(Q(wheelwidth__range=front_wheelwidth))
            elif not front_wheelwidth and rear_wheelwidth:
                rear_wheelwidth = [float(i.strip()) for i in rear_wheelwidth.split(',')]
                sqs = sqs.filter(Q(wheelwidth__range=rear_wheelwidth))
            elif front_wheelwidth and rear_wheelwidth:
                front_wheelwidth = [float(i.strip()) for i in front_wheelwidth.split(',')]
                rear_wheelwidth = [float(i.strip()) for i in rear_wheelwidth.split(',')]
                sqs = sqs.filter(Q(wheelwidth__range=front_wheelwidth) |\
                                 Q(wheelwidth__range=rear_wheelwidth))

        # Boltpattern
        boltpattern = cleaned_data['boltpattern']
        if boltpattern:
            sqs = sqs.filter(Q(boltpattern_1=boltpattern) |\
                             Q(boltpattern_2=boltpattern))

        # Offset
        offset_min = cleaned_data['offset_min']
        offset_max = cleaned_data['offset_max']
        front_offset = cleaned_data['front_offset']
        rear_offset = cleaned_data['rear_offset']

        if offset_min and offset_max:
            sqs = sqs.filter(offset__gte=offset_min, offset__lte=offset_max)
        if offset_min and not offset_max:
            sqs = sqs.filter(offset__gte=offset_min)
        if offset_max and not offset_min:
            sqs = sqs.filter(offset__lte=offset_max)
        if front_offset and not rear_offset:
            front_offset = [int(i.strip()) for i in front_offset.split(',')]
            sqs = sqs.filter(Q(offset__range=front_offset))
        if rear_offset and not front_offset:
            rear_offset = [int(i.strip()) for i in rear_offset.split(',')]
            sqs = sqs.filter(Q(offset__range=rear_offset))
        if front_offset and rear_offset:
            front_offset = [int(i.strip()) for i in front_offset.split(',')]
            rear_offset = [int(i.strip()) for i in rear_offset.split(',')]
            sqs = sqs.filter(Q(offset__range=front_offset) |\
                             Q(offset__range=rear_offset))

        # Finish
        finish = cleaned_data['finish']
        if finish:
            sqs = sqs.filter(finish=finish)

        return sqs

class VehicleSearch(forms.Form):
    manufacturer = forms.ModelChoiceField(queryset=WheelManufacturer.objects.visible(), required=False)
    finish = forms.ModelChoiceField(queryset=Finish.objects.all(), required=False)
    price_from = forms.CharField(required=False)
    price_to = forms.CharField(required=False)
    diameter = forms.ChoiceField(choices=DIAMETERS, required=False)



class WheelReviewForm(BaseReviewForm):

    def __init__(self, *args, **kwargs):
        self.reviewer = kwargs.pop('reviewer', None)
        super(WheelReviewForm, self).__init__(*args, **kwargs)
        if self.reviewer.is_authenticated and self.reviewer.is_active:
            self.fields['name'].widget = forms.HiddenInput()

    class Meta:
        model = WheelReview
        exclude = ('reviewee', 'reviewer', 'ip', 'is_approved',)

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        reviewer = self.reviewer

        if not name:
            if not (reviewer.is_authenticated and reviewer.is_active):
                errors = self._errors.setdefault("name", ErrorList())
                errors.append("Your name is required.")


class WheelCustomerMediaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(WheelCustomerMediaForm, self).__init__(*args, **kwargs)

        for field in self.fields.items():
            self.fields[field[0]].label = mark_safe("{0}<span>{1}</span>".format(
                unicode(self.fields[field[0]].label),
                unicode(self.fields[field[0]].help_text)
            ))

            if isinstance(field[1], forms.CharField) or\
               isinstance(field[1], forms.IntegerField):
                self.fields[field[0]].widget.attrs['class'] = 'textInput'

    class Meta:
        model = WheelCustomerMedia
        exclude = ('user', 'wheel', 'is_active')

    '''
    def clean_video(self):
        video = self.cleaned_data.get('video', '')
        if video:
            try:
                yt_key = dict(parse_qsl(urlparse(video).query))['v']
            except:
                yt_key = ''
            return yt_key
    '''

    def clean(self):
        cleaned_data = self.cleaned_data
        picture = cleaned_data.get("picture")
        video = cleaned_data.get("video")

        '''
        if picture and video:
            raise forms.ValidationError("Please upload either a picture or a video but not both.")
        '''

        if not picture and not video:
            raise forms.ValidationError("Please upload either a picture or a video.")

        return cleaned_data

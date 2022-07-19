from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe

from haystack.query import SearchQuerySet
from haystack.forms import SearchForm

from kxwheels.apps.reviews.forms import BaseReviewForm, RatingWidgetRenderer
from kxwheels.apps.kx.models import (TireCategory, TireManufacturer, TireCustomerMedia, TireSize, TireReview)
from kxwheels.apps.vehicle.models import (TreadWidth, Profile, Diameter)

'''
TREADWIDTHS = [(t.value, t.value) for t in TreadWidth.objects.all().order_by('ordering')]
PROFILES = [(p.value, p.value) for p in Profile.objects.all().order_by('ordering')]
DIAMETERS = [(d.value, d.value) for d in Diameter.objects.all().order_by('ordering')]
CATEGORIES = [(c.name, c.name) for c in TireCategory.objects.all()]
MANUFACTURERS = [(m.name, m.name) for m in TireManufacturer.objects.visible()]

TREADWIDTHS.insert(0, ('','---------'))
PROFILES.insert(0, ('','---------'))
DIAMETERS.insert(0, ('','---------'))
CATEGORIES.insert(0, ('','---------'))
MANUFACTURERS.insert(0, ('','---------'))
'''

PREFIX_CHOICES = (
    ('', '---------'),
    ('P', 'P'),
    ('LT', 'LT'),
)

PRICE_CHOICES = (
    ('(1.00,100.00)', '< 100'),
    ('(101.00,200.00)', '101 - 200'),
    ('(201.00,300.00)', '201 - 300'),
    ('(301.00,400.00)', '301 - 400'),
    ('(500.00,1000.00)', '500 >'),
)

LOAD_RATING_CHOICES = (
    ('(71,80)', '71 - 80'),
    ('(81,90)', '81 - 90'),
    ('(91,100)', '91 - 100'),
    ('(101,110)', '101 - 110'),
)

class TireSizeSearchForm(SearchForm):
    q = forms.CharField(max_length=1000, initial='*', widget=forms.HiddenInput())
    sku = forms.CharField(label=_("Manufacturer SKU / Part #"), max_length=20, required=False)
    prefix = forms.ChoiceField(label=_("Prefix"), choices=PREFIX_CHOICES, required=False)

    treadwidth = forms.ModelChoiceField(
        label=_("Treadwidth"),
        to_field_name="value",
        queryset=TreadWidth.objects.all().order_by('ordering'),
        required=False,
    )

    profile = forms.ModelChoiceField(
        label=_("Profile"),
        to_field_name="value",
        queryset=Profile.objects.all().order_by('ordering'),
        required=False,
    )

    diameter = forms.ModelChoiceField(
        label=_("Diameter"),
        to_field_name="value",
        queryset=Diameter.objects.all().order_by('ordering'),
        required=False,
    )

    category = forms.ModelChoiceField(
        label=_('Category'), queryset=TireCategory.objects.all(),
        to_field_name="name",
        required=False, #widget=forms.CheckboxSelectMultiple,
    )

    manufacturer = forms.ModelChoiceField(
        label=_('Manufacturer'),
        to_field_name="name",
        queryset=TireManufacturer.objects.visible(),
        required=False, #widget=forms.CheckboxSelectMultiple(),
    )

    load_rating_range = forms.CharField(
        max_length=20, required=False,
        widget=forms.Select(choices=LOAD_RATING_CHOICES, attrs={'size':5,}),
    )

    ply = forms.ChoiceField(
        required=False, #widget=forms.RadioSelect(),
        choices=TireSize.PLY_CHOICES,
    )

    speed_rating = forms.ChoiceField(
        TireSize.SPEED_RATING_CHOICES,
        required=False,
        widget=forms.RadioSelect(),
        #widget=forms.CheckboxSelectMultiple,
    )

    price_range = forms.CharField(
        max_length=20, required=False,
        widget=forms.Select(choices=PRICE_CHOICES, attrs={'size':7}),
    )

    def search(self):
        cleaned_data = getattr(self, 'cleaned_data', None)
        sqs = SearchQuerySet().models(TireSize)

        if cleaned_data is None:
            return sqs

        # Prefix
        prefix = cleaned_data['prefix']
        if prefix:
            sqs = sqs.filter(prefix=prefix)

        # SKU
        sku = cleaned_data['sku']
        if sku:
            sqs = sqs.filter(sku=sku)

        # Category
        category = cleaned_data['category']
        if category:
            sqs = sqs.filter(category=category)

        # Manufacturer
        manufacturer = cleaned_data['manufacturer']
        if manufacturer:
            sqs = sqs.filter(manufacturer=manufacturer)

        # Treadwidth
        treadwidth = cleaned_data['treadwidth']
        if treadwidth:
            sqs = sqs.filter(treadwidth=treadwidth)

        # Profile
        profile = cleaned_data['profile']
        if profile:
            sqs = sqs.filter(profile=profile)

        # Diameter
        diameter = cleaned_data['diameter']
        if diameter:
            sqs = sqs.filter(diameter=diameter)

        # Speed rating
        speed_rating = cleaned_data['speed_rating']
        if speed_rating:
            sqs = sqs.filter(speed_rating=speed_rating)

        # Ply
        ply = cleaned_data['ply']
        if ply:
            sqs = sqs.filter(ply=ply)


            # Load rating
            #load_rating_range = cleaned_data['load_rating_range']
            #if load_rating_range:
            #    load_rating_range = tuple(load_rating_range[1:-1].split(','))
            #    print load_rating_range
            #    sqs = sqs.filter(load_rating__range=load_rating_range)

            # Price
            #price_range = cleaned_data['price_range']
            #if price_range:
            #    pr = map(Decimal, tuple(price_range[1:-1].split(',')))
            #    sqs = sqs.filter(price__range=pr)
            #sqs = sqs.raw_search('price:[%s TO %s]' % (pr[0], pr[1]))

        return sqs


class StaggeredSearchForm(SearchForm):
    q = forms.CharField(max_length=100, initial='*', widget=forms.HiddenInput())

    prefix_front = forms.ChoiceField(label=_("Prefix Front"), choices=PREFIX_CHOICES, required=False)

    treadwidth_front = forms.ModelChoiceField(
        label=_("Treadwidth Front"),
        to_field_name="value",
        queryset=TreadWidth.objects.all().order_by('ordering'),
    )

    profile_front = forms.ModelChoiceField(
        label=_("Profile Front"),
        to_field_name="value",
        queryset=Profile.objects.all().order_by('ordering'),
    )

    diameter_front = forms.ModelChoiceField(
        label=_("Diameter Front"),
        to_field_name="value",
        queryset=Diameter.objects.all().order_by('ordering'),
    )

    treadwidth_rear = forms.ModelChoiceField(
        label=_("Treadwidth Rear"),
        to_field_name="value",
        queryset=TreadWidth.objects.all().order_by('ordering'),
    )

    profile_rear = forms.ModelChoiceField(
        label=_("Profile Rear"),
        to_field_name="value",
        queryset=Profile.objects.all().order_by('ordering'),
    )

    diameter_rear = forms.ModelChoiceField(
        label=_("Diameter Rear"),
        to_field_name="value",
        queryset=Diameter.objects.all().order_by('ordering'),
    )

    prefix_rear = forms.ChoiceField(label=_("Prefix Rear"), choices=PREFIX_CHOICES, required=False)

    def search(self):
        cleaned_data = getattr(self, 'cleaned_data', None)
        sqs = SearchQuerySet().models(TireSize)

        if cleaned_data is None:
            return sqs.filter(pk=0)

        # Prefixes
        prefixes = (cleaned_data['prefix_front'], cleaned_data['prefix_rear'])
        if prefixes:
            sqs = sqs.filter(prefixes__in=prefixes)

        # Treadwidth
        treadwidths = (cleaned_data['treadwidth_front'], cleaned_data['treadwidth_rear'])
        if treadwidths:
            sqs = sqs.filter(treadwidth__in=treadwidths)

        # Profile
        profiles = (cleaned_data['profile_front'], cleaned_data['profile_rear'])
        if profiles:
            sqs = sqs.filter(profile__in=profiles)

        # Diameter
        diameters = (cleaned_data['diameter_front'], cleaned_data['diameter_rear'])
        if diameters:
            sqs = sqs.filter(diameter__in=diameters)

        return sqs



class TireReviewForm(BaseReviewForm):

    dry_rating = forms.IntegerField(label=_('Dry/Hot weather'),
        help_text=_('Dry Traction when accelerating, \
                                    braking, cornering.'),
        min_value=1,
        max_value=5,
        widget=forms.RadioSelect(
            renderer=RatingWidgetRenderer,
            choices=TireReview.GENERIC_RATING_CHOICES))

    noise_rating = forms.IntegerField(label=_('Noise from tire'),
        help_text=_('Noise/Tone of tire, 1 for \
                                      loud/aggressive tires.'),
        min_value=1,
        max_value=5,
        widget=forms.RadioSelect(
            renderer=RatingWidgetRenderer,
            choices=TireReview.GENERIC_RATING_CHOICES))

    offroad_rating = forms.IntegerField(label=_('Offroad'),
        help_text=_('Traction in Offroad conditions, \
                                        rocky, muddy, etc.'),
        min_value=1,
        max_value=5,
        widget=forms.RadioSelect(
            renderer=RatingWidgetRenderer,
            choices=TireReview.GENERIC_RATING_CHOICES))

    wet_rating = forms.IntegerField(label=_('Rain/Wet conditions'),
        help_text=_('Wet traction when \
                                             accelerating, braking and cornering.'),
        min_value=1,
        max_value=5,
        widget=forms.RadioSelect(
            renderer=RatingWidgetRenderer,
            choices=TireReview.GENERIC_RATING_CHOICES))

    comfort_rating = forms.IntegerField(label=_('Ride comfort'),
        help_text=_('Ride comfort - as the feel \
                                        of the tires.'),
        min_value=1,
        max_value=5,
        widget=forms.RadioSelect(
            renderer=RatingWidgetRenderer,
            choices=TireReview.GENERIC_RATING_CHOICES))

    snow_rating = forms.IntegerField(label=_('Snow/Ice'),
        help_text=_('Traction when accelerating, \
                                     braking and cornering in shallow (up to \
                                     about 4 inches), powder snow.'),
        min_value=1,
        max_value=5,
        widget=forms.RadioSelect(
            renderer=RatingWidgetRenderer,
            choices=TireReview.GENERIC_RATING_CHOICES))

    treadwear_rating = forms.IntegerField(label=_('Treadwear/Age'),
        help_text=_('Expectation of wear on \
                                          the tires.'),
        min_value=1,
        max_value=5,
        widget=forms.RadioSelect(
            renderer=RatingWidgetRenderer,
            choices=TireReview.GENERIC_RATING_CHOICES))

    def __init__(self, *args, **kwargs):
        self.reviewer = kwargs.pop('reviewer', None)
        super(TireReviewForm, self).__init__(*args, **kwargs)
        if self.reviewer.is_authenticated and self.reviewer.is_active:
            self.fields['name'].widget = forms.HiddenInput()

    class Meta:
        model = TireReview
        exclude = ('reviewee', 'reviewer', 'ip', 'is_approved',)

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        reviewer = self.reviewer

        if not name:
            if not (reviewer.is_authenticated and reviewer.is_active):
                errors = self._errors.setdefault("name", ErrorList())
                errors.append("Your name is required.")
        return name

class TireCustomerMediaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(TireCustomerMediaForm, self).__init__(*args, **kwargs)

        for field in self.fields.items():
            self.fields[field[0]].label = mark_safe("{0}<span>{1}</span>".format(
                unicode(self.fields[field[0]].label),
                unicode(self.fields[field[0]].help_text)
            ))

            if isinstance(field[1], forms.CharField) or\
               isinstance(field[1], forms.IntegerField):
                self.fields[field[0]].widget.attrs['class'] = 'textInput'

    class Meta:
        model = TireCustomerMedia
        exclude = ('user', 'tire', 'is_active')


    def clean(self):
        cleaned_data = self.cleaned_data
        picture = cleaned_data.get("picture")
        video = cleaned_data.get("video")

        if picture and video:
            raise forms.ValidationError("Please upload either a picture or a video but not both.")

        if not picture and not video:
            raise forms.ValidationError("Please upload either a picture or a video.")

        return cleaned_data

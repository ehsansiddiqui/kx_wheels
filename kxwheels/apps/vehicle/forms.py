import datetime

from django import forms

from haystack.forms import SearchForm
from haystack.query import SearchQuerySet
from kxwheels.apps.vehicle.models import (Manufacturer, Model, Diameter)

MAKES = [(m.get('name'), m.get('name')) for m in Manufacturer.objects.values('slug', 'name').order_by('name')]
# (Very costly) YEARS = [(m.get('year'), m.get('year')) for m in Model.objects.values('year').distinct().order_by('-year')]
YEARS = [(y, y) for y in range(datetime.datetime.now().year + 1, 1964, -1)]
#DIAMETER = [(20, 20),(22, 22)]

MAKES.insert(0, ('','- Make -'))
YEARS.insert(0, ('','- Year -'))

class ModelSearchForm(SearchForm):

    q = forms.CharField(max_length=100, initial='*', widget=forms.HiddenInput())
    make = forms.ChoiceField(choices=MAKES, required=False)
    year = forms.ChoiceField(choices=YEARS, required=False)
    model = forms.CharField(max_length=255, widget=forms.Select, required=False)
    #diameter = forms.ChoiceField(choices=DIAMETER, required=True)

    def search(self):
        cleaned_data = getattr(self, 'cleaned_data', None)
        sqs = SearchQuerySet().models(Model)
        
        if not cleaned_data:
            return sqs

        # Manufacturer
        manufacturer = cleaned_data['make']
        if manufacturer:
            sqs = sqs.filter(manufacturer=manufacturer)
        
        # Year
        year = cleaned_data['year'] 
        if year:
            sqs = sqs.filter(year=year)
            
        # Name
        name = cleaned_data['model']
        if name:
            sqs = sqs.filter(name=name)

        # Diameter
        #diameter = cleaned_data['diameter']
        #if name:
         #   sqs = sqs.filter(diameter=diameter)
        return sqs
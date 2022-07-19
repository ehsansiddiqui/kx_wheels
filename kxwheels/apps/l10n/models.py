# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

CONTINENTS = (
    ('AF', _('Africa')),
    ('NA', _('North America')),
    ('EU', _('Europe')),
    ('AS', _('Asia')),
    ('OC', _('Oceania')),
    ('SA', _('South America')),
    ('AN', _('Antarctica'))
)

AREAS = (
    ('a', _('Another')),
    ('i', _('Island')),
    ('ar', _('Arrondissement')),
    ('at', _('Atoll')),
    ('ai', _('Autonomous island')),
    ('ca', _('Canton')),
    ('cm', _('Commune')),
    ('co', _('County')),
    ('dp', _('Department')),
    ('de', _('Dependency')),
    ('dt', _('District')),
    ('dv', _('Division')),
    ('em', _('Emirate')),
    ('gv', _('Governorate')),
    ('ic', _('Island council')),
    ('ig', _('Island group')),
    ('ir', _('Island region')),
    ('kd', _('Kingdom')),
    ('mu', _('Municipality')),
    ('pa', _('Parish')),
    ('pf', _('Prefecture')),
    ('pr', _('Province')),
    ('rg', _('Region')),
    ('rp', _('Republic')),
    ('sh', _('Sheading')),
    ('st', _('State')),
    ('sd', _('Subdivision')),
    ('sj', _('Subject')),
    ('ty', _('Territory')),
)

POSTAL_TYPES = (
    ('postal_code', 'Postal Code'),
    ('zip', 'Zip Code'),
    ('postcode', 'Postcode'),
)

class Country(models.Model):
    """
    International Organization for Standardization (ISO) 3166-1 Country list
    """
    iso_3166_1 = models.CharField(_('ISO 3166-1 alpha-2'), primary_key=True, max_length=10)
    name = models.CharField(_('official name'), max_length=128)
    formal_name = models.CharField(_('formal name'), max_length=128)
    active = models.BooleanField(_('is active'), default=True)
    continent = models.CharField(_('continent'), max_length=2, choices=CONTINENTS, blank=True, null=True)
    admin_area = models.CharField(_('administrative area'), choices=AREAS, max_length=128, null=True, blank=True)
    postal_type = models.CharField(_('postal type'), choices=POSTAL_TYPES, max_length=128, null=True, blank=True)

    class Meta:
        verbose_name = _('country')
        verbose_name_plural = _('countries')
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class AdminArea(models.Model):
    """
    Administrative Area level 1 for a country.  For the US, this would be the states
    """
    iso_3166_1 = models.ForeignKey(Country)
    iso_3166_2 = models.CharField(_('ISO 3166-2 Postal Abbreviation'), primary_key=True, max_length=128, blank=True)
    name = models.CharField(_('admin area name'), max_length=60, )
    active = models.BooleanField(_('is active'), default=True)

    class Meta:
        verbose_name = _('administrative area')
        verbose_name_plural = _('administrative areas')
        ordering = ('name',)
        unique_together = (('iso_3166_1', 'iso_3166_2'),)

    def __unicode__(self):
        return self.name

class City(models.Model):
    """
    City for an Admin Area of a country.
    """
    iso_3166_2 = models.ForeignKey(AdminArea)
    name = models.CharField(_('city name'), max_length=255,)

    class Meta:
        verbose_name_plural = _('cities')
        ordering = ('name',)

    def __unicode__(self):
        return self.name

class PostalCode(models.Model):
    """
    Postal codes of cities
    """
    postal_code = models.CharField(_('postal code'), max_length=10, unique=True)
    city = models.ForeignKey(City)
    iso_3166_2 = models.ForeignKey(AdminArea)
    location = models.CharField(_('location point'), max_length=40, blank=True, null=True,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.postal_code
        
        
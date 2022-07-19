from django.core.cache import cache
from django.db import models
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail import ImageField

from kxwheels.apps.shop.models import HardProduct
from kxwheels.apps.vehicle.utils import slugify


# Abstract models #
class TireSize(models.Model):
    prefix = models.CharField(max_length=5, blank=True, null=True, default="")
    treadwidth = models.CharField(max_length=6)
    profile = models.CharField(max_length=6)
    additional_size = models.CharField(max_length=5, blank=True,
                                       null=True, default="")
    diameter = models.CharField(max_length=6)

    class Meta:
        abstract = True

    @property
    def tpd(self):
        return '{0}{1}/{2}-{3}{4}'.format(self.prefix,
                                          self.treadwidth,
                                          self.profile,
                                          self.additional_size,
                                          self.diameter)

    @property
    def querystring(self):
        # TODO: Remove upper() on prefix
        return u'prefix={0}&treadwidth={1}&profile={2}&diameter={3}'.format(
            self.prefix.upper(), self.treadwidth, self.profile, self.diameter)
        
class StaggeredTireSize(models.Model):
    front_prefix = models.CharField(max_length=5, blank=True, null=True, default="")
    front_treadwidth = models.CharField( max_length=6)
    front_profile = models.CharField(max_length=6)
    front_additional_size = models.CharField(max_length=5, blank=True,
                                             null=True, default="")
    front_diameter = models.CharField(max_length=6)

    rear_prefix = models.CharField(max_length=5, blank=True, null=True, default="")
    rear_treadwidth = models.CharField( max_length=6)
    rear_profile = models.CharField(max_length=6)
    rear_additional_size = models.CharField(max_length=5, blank=True,
                                            null=True, default="")
    rear_diameter = models.CharField(max_length=6)
    
    class Meta:
        abstract = True
        
    @property
    def front_tpd(self):
        return '{0}{1}/{2}-{3}{4}'.format(self.front_prefix,
                                          self.front_treadwidth,
                                          self.front_profile,
                                          self.front_additional_size,
                                          self.front_diameter)

    @property
    def rear_tpd(self):
        return '{0}{1}/{2}-{3}{4}'.format(self.rear_prefix,
                                          self.rear_treadwidth,
                                          self.rear_profile,
                                          self.rear_additional_size,
                                          self.rear_diameter)

    @property
    def querystring(self):
        return u'prefix_front={0}&treadwidth_front={1}&profile_front={2}&diameter_front={3}&\
prefix_rear={4}&treadwidth_rear={5}&profile_rear={6}&diameter_rear={7}'.format(
            self.front_prefix, self.front_treadwidth, self.front_profile, self.front_diameter,
            self.rear_prefix, self.rear_treadwidth, self.rear_profile, self.rear_diameter,)


class WheelSize(models.Model):
    diameter_range = models.CharField(_('diameter range'), max_length=50, blank=True, null=True)
    wheelwidth_range = models.CharField(_('wheel width range'), max_length=50, blank=True, null=True)
    offset_range = models.CharField(_('offset range'), max_length=50, blank=True, null=True)

    class Meta:
        abstract = True
        
    def to_dict(self):
        return {
            'diameter_range': self.diameter_range,
            'wheelwidth_range': self.wheelwidth_range,
            'offset_range': self.offset_range,
        }
# End abstract models #


# Different models. Will describe later
class TreadWidth(models.Model):
    value = models.CharField(_('value'), max_length=6, unique=True)
    ordering = models.IntegerField(_('sort order'), blank=True, null=True)

    class Meta:
        verbose_name = _('treadwidth')
        verbose_name_plural = _('treadwidths') 
        
    def __unicode__(self):
        return u'%s' % self.value

class Profile(models.Model):
    value = models.CharField(_('value'), max_length=6, unique=True)
    ordering = models.IntegerField(_('sort order'), blank=True, null=True)

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles') 
    
    def __unicode__(self):
        return u'%s' % self.value

class Diameter(models.Model):
    value = models.CharField(_('value'), max_length=6, unique=True)
    ordering = models.IntegerField(_('sort order'), blank=True, null=True)

    class Meta:
        verbose_name = _('diameter')
        verbose_name_plural = _('diameters') 

    def __unicode__(self):
        return u'%s' % self.value
    
class BoltPattern(models.Model):
    value = models.CharField("Value", max_length=10, unique=True)
    sort_order = models.IntegerField("Sort order", blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.value

    class Meta:
        ordering = ('id',)
        verbose_name = "bolt pattern"
        verbose_name_plural = "bolt patterns" 

class WheelWidth(models.Model):
    value = models.CharField("Value", max_length=6, unique=True)
    sort_order = models.IntegerField("Sort order", blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.value

    class Meta:
        verbose_name = "wheel width"
        verbose_name_plural = "wheel widths" 
        
class Finish(models.Model):
    value = models.CharField("Value", max_length=50, unique=True)
    sort_order = models.IntegerField("Sort order", blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.value

    class Meta:
        verbose_name = "finish"
        verbose_name_plural = "finishes"
        ordering = ("value",)

# End different models


class Manufacturer(models.Model):
    name = models.CharField(_('name'), max_length=200)
    description = models.TextField(_('description'), blank=True, null=True)
    slug = models.SlugField(_('slug'), max_length=255, blank=True, unique=True)
    picture = ImageField(_('picture'), upload_to='pictures/vehicles/manufacturer',
        blank=True, null=True)
    ordering = models.IntegerField(_('sort order'), blank=True, null=True)
    is_active = models.BooleanField(default=1)
    
    class Meta:
        ordering = ['name']
        verbose_name = _('manufacturer')
        verbose_name_plural = _('manufacturers')
    
    def __unicode__(self):
        return self.name
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, instance=self)
        super(Manufacturer, self).save(*args, **kwargs)

class ModelManager(models.Manager):
    def active(self, **kwargs):
        return self.filter(is_active=True, **kwargs)

class Model(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, verbose_name=_('manufacturer'), related_name="models")
    name = models.CharField(_('model'), max_length=200)
    year = models.IntegerField(_('year'))
    slug = models.SlugField(_('slug'), max_length=255, blank=True, unique=True)
    boltpattern = models.CharField(_('bolt pattern'), max_length=50, blank=True,)
    centerbore = models.CharField(_('centerbore'), max_length=6, blank=True, null=True,)
    ordering = models.IntegerField(_('sort order'), blank=True, null=True)
    is_active = models.BooleanField(default=1)
    
    class Meta:
        ordering = ['name']
        verbose_name = _('model')
        verbose_name_plural = _('models')
        unique_together = ('manufacturer', 'name', 'year')
    
    def __unicode__(self):
        return u'%s %s %s' % (self.year, self.manufacturer.name, self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify("%s-%s" % (self.year, self.name), instance=self)
        super(Model, self).save(*args, **kwargs)

    def get_front_wheel_size(self):
        try:
            _obj = self.front_wheel_size
        except FrontWheelSize.DoesNotExist:
            return None
        else:
            return _obj
    
    def get_rear_wheel_size(self):
        try:
            _obj = self.rear_wheel_size
        except RearWheelSize.DoesNotExist:
            return None
        else:
            return _obj
    
    def get_oe_tire_sizes(self):
        return self.oe_tire_sizes.all()

    def get_oe_staggered_tire_sizes(self):
        return self.oe_staggered_tire_sizes.all()

    def get_plus_tire_sizes(self):
        return self.plus_tire_sizes.all()

    def get_plus_staggered_tire_sizes(self):
        return self.plus_staggered_tire_sizes.all()

    @classmethod
    def get_cache_key(cls, request):
        return u"{}_vehicle".format(request.user.pk)

    @classmethod
    def get_from_cache(cls, request):
        cache_key = cls.get_cache_key(request)
        return cache.get(cache_key)


# Wheel size
class FrontWheelSize(WheelSize):
    model = models.OneToOneField(Model, related_name="front_wheel_size")
    
    class Meta:
        verbose_name = _('Front Wheel Size')
        verbose_name_plural = _('Front Wheel Sizes')
    
    def __unicode__(self):
        return 'Front Wheel Size'

class RearWheelSize(WheelSize):
    model = models.OneToOneField(Model, related_name="rear_wheel_size")
    
    class Meta:
        verbose_name = _('Rear Wheel Size')
        verbose_name_plural = _('Rear Wheel Sizes')
    
    def __unicode__(self):
        return 'Rear Wheel Size'
# End Wheel size

# Tire sizes
class OETireSize(TireSize):
    model = models.ForeignKey(Model, related_name="oe_tire_sizes")

    class Meta:
        verbose_name = _('OE Tire Size')
        verbose_name_plural = _('OE Tire Sizes')
    
    def __unicode__(self):
        return 'OE Tire Size - %s/%s-%s' % (self.treadwidth, self.profile, self.diameter)
        
class OEStaggeredTireSize(StaggeredTireSize):
    model = models.ForeignKey(Model, related_name="oe_staggered_tire_sizes")
    
    class Meta:
        verbose_name = _('OE Staggered Tire Size')
        verbose_name_plural = _('OE Staggered Tire Sizes')
    
    def __unicode__(self):
        return 'OE Staggered Tire Size'
    
class PlusTireSize(TireSize):
    model = models.ForeignKey(Model, related_name="plus_tire_sizes")
    
    class Meta:
        verbose_name = _('Plus Tire Size')
        verbose_name_plural = _('Plus Tire Sizes')
    
    def __unicode__(self):
        return 'Plus Tire Size - %s' % (self.tpd)
    
class PlusStaggeredTireSize(StaggeredTireSize):
    model = models.ForeignKey(Model, related_name="plus_staggered_tire_sizes")
    
    class Meta:
        verbose_name = _('Plus Staggered Tire Size')
        verbose_name_plural = _('Plus Staggered Tire Sizes')
    
    def __unicode__(self):
        return 'Plus Staggered Tire Size - %s - %s' % (self.front_tpd, self.rear_tpd)
# End Tire sizes


class TPMS(HardProduct):
    vehicle = models.OneToOneField(Model, verbose_name=_('vehicle'), related_name='tpms')
    sensor = models.CharField(_('sensor'), max_length=200)

    class Meta:
        abstract = False

    def get_price(self, user=None):
        price = self.price
        if user is None:
            return self.price

        #TODO: TPMS discount

        return price

    def __unicode__(self):
        return "{0} - {1}".format(
            self.vehicle, self.sensor
        )

from urlparse import urlparse

from django.db import models
from django.db.models import Q, Avg
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from sorl.thumbnail import ImageField
from sorl.thumbnail.shortcuts import get_thumbnail
from crequest.middleware import CrequestMiddleware

from kxwheels.apps.shop.models import HardProduct
from kxwheels.apps.reviews.models import BaseReview

from kxwheels.apps.kx.models import StandardModel
from kxwheels.apps.kx.utils import cut_decimals, slugify, slugify_uuid, extract_subdomain

from kxwheels.apps.account.models import Profile


class TireCategory(StandardModel):
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True)
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), max_length=100, unique=True)
    picture = ImageField(_('picture'), upload_to='media/categories',
                         blank=True, null=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, instance=self)
        super(TireCategory, self).save(*args, **kwargs)

    class Meta:
        app_label = "kx"
        verbose_name = _('category')
        verbose_name_plural = _('categories')


class ManufacturerManager(models.Manager):
    def get_query_set(self):
        return super(ManufacturerManager, self).get_query_set().order_by('name')

    def visible(self):
        hidden_manufacturers = None
        request = CrequestMiddleware.get_request()
        subdomain, subdomain_profile = extract_subdomain(request)

        if subdomain and subdomain_profile:
            user = subdomain_profile.user
            hidden_manufacturers = TireManufacturerDiscount.objects.filter(
                user=user,
                is_visible=False
            ).values('manufacturer')

        if hidden_manufacturers:
            return self.filter(~Q(pk__in=hidden_manufacturers))
        else:
            return self.all()


class TireManufacturer(StandardModel):
    name = models.CharField(_('name'), max_length=200)
    description = models.TextField(_('description'), blank=True)
    slug = models.SlugField(_('slug'), max_length=255, blank=True, unique=True)
    picture = ImageField(_('picture'), upload_to='media/manufacturers', blank=True, null=True)
    warranty = models.TextField(_('warranty'), blank=True, null=True)

    objects = ManufacturerManager()

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('tire_tire_list', [self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, instance=self)
        super(TireManufacturer, self).save(*args, **kwargs)

    class Meta:
        app_label = "kx"
        ordering = ['name']
        verbose_name = _('tire manufacturer')
        verbose_name_plural = _('tire manufacturers')


class TireManufacturerDiscount(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'), related_name='tire_discounts')
    manufacturer = models.ForeignKey(TireManufacturer, verbose_name=_('manufacturer'), related_name='discounts')
    discount = models.IntegerField(_('discount'), default=13)
    is_visible = models.BooleanField(_('Is this brand visible to dealer?'), default=True)

    def __unicode__(self):
        return "%s - %s%%" % (self.manufacturer, self.discount)

    class Meta:
        app_label = "kx"
        verbose_name = _('tire manufacturer discount')
        verbose_name_plural = _('tire manufacturer discounts')


class DealerTireManufacturerDiscount(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'), related_name='dealer_tire_discounts')
    manufacturer = models.ForeignKey(TireManufacturer, verbose_name=_('manufacturer'), related_name='dealer_discounts')
    discount = models.IntegerField(_('discount'), default=13)

    def __unicode__(self):
        return "%s - %s%%" % (self.manufacturer, self.discount)

    class Meta:
        app_label = "kx"
        verbose_name = _('dealer_tire manufacturer discount')
        verbose_name_plural = _('dealer_tire manufacturer discounts')


class Tire(StandardModel):
    manufacturer = models.ForeignKey(TireManufacturer, verbose_name=_('manufacturer'), related_name='tires')
    category = models.ForeignKey(TireCategory, verbose_name=_('category'), related_name='tires')
    name = models.CharField(_('name'), max_length=200)
    slug = models.SlugField(_('slug'), max_length=255, blank=True, unique=True)
    description = models.TextField(_('description'), blank=True)

    dry_rating = models.DecimalField(_('dry rating'), max_digits=3, decimal_places=2, blank=True, null=True)
    wet_rating = models.DecimalField(_('wet rating'), max_digits=3, decimal_places=2, blank=True, null=True)
    snow_rating = models.DecimalField(_('snow rating'), max_digits=3, decimal_places=2, blank=True, null=True)
    handling_rating = models.DecimalField(_('handling rating'), max_digits=3, decimal_places=2, blank=True, null=True)
    comfort_rating = models.DecimalField(_('comfort rating'), max_digits=3, decimal_places=2, blank=True, null=True)
    noise_rating = models.DecimalField(_('noise rating'), max_digits=3, decimal_places=2, blank=True, null=True)
    treadwear_rating = models.DecimalField(_('treadwear rating'), max_digits=3, decimal_places=2, blank=True, null=True)

    def __unicode__(self):
        return unicode(self.name)

    @models.permalink
    def get_absolute_url(self):
        return ('tire_tire_detail', [self.manufacturer.slug, self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_uuid(self.name)
        super(Tire, self).save(*args, **kwargs)

    def get_num_reviews(self):
        return TireReview.objects.filter(reviewee=self).count()

    def get_average_review(self):
        return TireReview.objects.filter(reviewee=self).aggregate(Avg('rating'))['rating__avg'] or -1

    class Meta:
        app_label = "kx"
        ordering = ['name']
        verbose_name = _('tire')
        verbose_name_plural = _('tires')
        unique_together = ('manufacturer', 'name')

    @property
    def thumbnail(self):
        try:
            result = self.pictures.all()[0].picture
        except IndexError:
            result = None
        return result


class TireCoupon(models.Model):
    tire = models.ForeignKey(Tire, related_name='coupons')
    picture = ImageField(_('picture'), upload_to='media/coupons', )
    detail = models.TextField(_('coupon details'), blank=True, null=True)

    is_active = models.BooleanField()

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def __unicode__(self):
        return self.picture

    class Meta:
        app_label = "kx"


class ActiveCustomerMediaManager(models.Manager):
    def get_query_set(self):
        return super(ActiveCustomerMediaManager, self).get_query_set().filter(is_active=True)


class TireCustomerMedia(models.Model):
    user = models.ForeignKey(User, verbose_name=_("uploader"), related_name="tire_media", )
    tire = models.ForeignKey(Tire, related_name='customer_media', )
    title = models.CharField(_('title'), max_length=100)
    make = models.CharField(_('make'), max_length=255)
    year = models.CharField(_('year'), max_length=255)
    model = models.CharField(_('model'), max_length=255)
    picture = ImageField(_('picture'), upload_to='media/customer', help_text="Max size is 250 KiB", blank=True,
                         null=True)
    video = models.URLField(_('video'), max_length=255, help_text="YouTube Video URL", blank=True, null=True)
    comment = models.TextField(_('comments'), max_length=500, blank=True, null=True)

    is_active = models.BooleanField()

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    objects = models.Manager()
    active = ActiveCustomerMediaManager()

    class Meta:
        app_label = "kx"


class TireSize(HardProduct):
    PREFIX_CHOICES = (
        ('P', 'P'),
        ('LT', 'LT')
    )

    PLY_CHOICES = (
        ('', '---'),
        ('6C', '6C'),
        ('8D', '8D'),
        ('10E', '10E'),
    )

    SPEED_RATING_CHOICES = (
        ('H', 'H'),
        ('P', 'P'),
        ('Q', 'Q'),
        ('R', 'R'),
        ('S', 'S'),
        ('T', 'T'),
        ('V', 'V'),
        ('W', 'W'),
        ('Y', 'Y'),
        ('Z', 'Z'),
    )

    AVAILABILITY_CHOICES = (
        (0, 'Manufacturer Direct'),
        (1, 'Ships in 1-2 Weeks'),
        (2, 'ETA 2-4 Weeks'),
        (3, 'Custom Build'),
        (4, 'Specialty Order'),
        (5, 'Call for Availability'),
    )

    tire = models.ForeignKey(Tire, verbose_name=_('tire'), related_name='sizes')
    part_no = models.CharField(_('part #'), max_length=100, blank=True, null=True)
    prefix = models.CharField(_('prefix'), max_length=5, choices=PREFIX_CHOICES, null=True)
    treadwidth = models.CharField(_('treadwidth'), max_length=6, blank=True, null=True, default="")
    profile = models.CharField(_('profile'), max_length=6, blank=True, null=True, default="")
    additional_size = models.CharField(_('additional size'), max_length=5, blank=True, null=True, default="")
    diameter = models.DecimalField(_('diameter'), max_digits=6, decimal_places=2, blank=True, null=True, default="")
    ply = models.CharField(_('ply'), max_length="5", choices=PLY_CHOICES, blank=True, default="")
    utgq_rating = models.CharField(_('UTGQ rating'), max_length=50, blank=True, default="")
    speed_rating = models.CharField(_('speed rating'), max_length=2, blank=True, choices=SPEED_RATING_CHOICES)
    load_rating = models.CharField(_('load rating'), max_length=10, blank=True, null=True)
    sidewall_style = models.CharField(_('sidewall style'), max_length=100, default="BW", blank=True, null=True)
    availability = models.IntegerField(_('availability'), choices=AVAILABILITY_CHOICES, blank=True, null=True)

    def __unicode__(self):
        return u'%s %s (%s %s/%s/%s)' % (
            self.tire.manufacturer,
            self.tire.name,
            self.prefix,
            self.treadwidth,
            self.profile,
            self.get_diameter(),
        )

    class Meta:
        app_label = "kx"
        ordering = ("diameter",)
        verbose_name = _('tire size')
        verbose_name_plural = _('tire sizes')

    @models.permalink
    def get_absolute_url(self):
        return ('tire_tiresize_detail', [self.tire.manufacturer.slug,
                                         self.tire.slug,
                                         self.pk])

    def save(self, *args, **kwargs):
        if self.pk and not self.sku:
            self.sku = 'T%s' % str(self.pk).zfill(10)
        if not self.short_desc:
            self.short_desc = "No description available"
        if not self.long_desc:
            self.long_desc = "No description available"
        if not self.name:
            self.name = self.__unicode__()
        super(TireSize, self).save(*args, **kwargs)

    def get_diameter(self):
        # return self.diameter
        return cut_decimals(self.diameter)

    def get_price(self, user=None, subdomain=None):
        """overriding get_price function to add discount"""
        if subdomain:
            subdomain_profile = Profile.objects.get(subdomain=subdomain)
        else:
            request = CrequestMiddleware.get_request()
            subdomain, subdomain_profile = extract_subdomain(request)

        discount = 0
        markup = 0
        try:
            if subdomain:
                if user != subdomain_profile.user:
                    markup = DealerTireManufacturerDiscount.objects.get(
                        manufacturer=self.tire.manufacturer,
                        user=subdomain_profile.user,
                    ).discount
        except:
            pass
        try:
            if subdomain:
                discount = TireManufacturerDiscount.objects.get(
                    manufacturer=self.tire.manufacturer,
                    user=subdomain_profile.user,
                ).discount
        except:
            pass

        price = str(round((self.price * (100 - discount) / 100 * (100 + markup) / 100) * 2, 1) / 2)
        return price

    @property
    def tpd(self):
        return "%s%s/%s%s%s" % (
            self.prefix,
            self.treadwidth,
            self.profile,
            self.additional_size,
            self.get_diameter(),
        )

    @property
    def thumbnail(self):
        try:
            result = self.tire.pictures.all()[0].picture
        except IndexError:
            result = None
        return result


class TirePicture(models.Model):
    tire = models.ForeignKey(Tire, verbose_name=_('tire'), related_name="pictures")
    picture = ImageField(_('picture'), upload_to='media/tires',
                         blank=True, null=True)
    caption = models.CharField(_('optional caption'), max_length=255, null=True, blank=True)

    class Meta:
        app_label = "kx"
        verbose_name = _('tire picture')
        verbose_name_plural = _('tire pictures')

    def save(self, *args, **kwargs):
        super(TirePicture, self).save(*args, **kwargs)

        # Generate thumbnails
        try:
            # - Large
            url = get_thumbnail(self.picture, '275x275').url
            thumbnail, created = TirePictureThumbnail.objects.get_or_create(
                tirepicture=self,
                size="lg",
            )
            url = urlparse(url)
            path = "{0}://{1}{2}".format(url.scheme, url.netloc, url.path)
            thumbnail.path = path
            thumbnail.save()

            # - Medium
            url = get_thumbnail(self.picture, '140x140').url
            thumbnail, created = TirePictureThumbnail.objects.get_or_create(
                tirepicture=self,
                size="med",
            )
            url = urlparse(url)
            path = "{0}://{1}{2}".format(url.scheme, url.netloc, url.path)
            thumbnail.path = path
            thumbnail.save()

            # - Small
            url = get_thumbnail(self.picture, '80x80').url
            thumbnail, created = TirePictureThumbnail.objects.get_or_create(
                tirepicture=self,
                size="sm",
            )
            url = urlparse(url)
            path = "{0}://{1}{2}".format(url.scheme, url.netloc, url.path)
            thumbnail.path = path
            thumbnail.save()
        except IOError, e:
            pass
            # TODO: Handle thumbnail creation failure properly


class TirePictureThumbnail(models.Model):
    tirepicture = models.ForeignKey(TirePicture, related_name="thumbnails")
    size = models.CharField(max_length=50)
    path = models.CharField(max_length=1000)

    class Meta:
        app_label = "kx"


class TireReview(BaseReview):
    GENERIC_RATING_CHOICES = (
        (1, 'Worse'),
        (2, 'Bad'),
        (3, 'Average'),
        (4, 'Good'),
        (5, 'Excellent'),
    )

    CONDITIONS_CHOICES = (
        (0, 'Offroad/Mud'),
        (1, 'Mostly Highway'),
        (2, 'Mostly City'),
        (3, 'Mixed City/Highway'),
        (4, 'Racing/Track'),
        (5, 'Only Winter'),
        (6, 'Load/Trailer Hauler'),
    )

    reviewee = models.ForeignKey(Tire, verbose_name=_('reviewee'), related_name="reviews", )
    reviewer = models.ForeignKey(User, verbose_name=_("reviewer"), related_name="tire_reviews",
                                 blank=True, null=True)

    make = models.CharField(_('make'), max_length=255)
    year = models.CharField(_('year'), max_length=255)
    model = models.CharField(_('model'), max_length=255)
    mileage = models.IntegerField(_('mileage'), blank=True, null=True,
                                  help_text=_('Distance travelled on tires'))

    dry_rating = models.PositiveIntegerField(_('Dry/Hot weather'),
                                             help_text=_('Dry Traction when accelerating, braking, cornering.'))
    noise_rating = models.PositiveIntegerField(_('Noise from tire'),
                                               help_text=_('Noise/Tone of tire, 1 for loud/aggressive tires.'))
    offroad_rating = models.PositiveIntegerField(_('Offroad'),
                                                 help_text=_('Traction in Offroad conditions, rocky, muddy, etc.'))
    wet_rating = models.PositiveIntegerField(_('Rain/Wet conditions'),
                                             help_text=_('Wet traction when accelerating, braking and cornering.'))
    comfort_rating = models.PositiveIntegerField(_('Ride comfort'),
                                                 help_text=_('Ride comfort - as the feel of the tires.'))
    snow_rating = models.PositiveIntegerField(_('Snow/Ice'),
                                              help_text=_('Traction when accelerating, braking and cornering \
                                             in shallow (up to about 4 inches), powder snow.'))
    treadwear_rating = models.PositiveIntegerField(_('Treadwear/Age'),
                                                   help_text=_('Expectation of wear on the tires.'))

    conditions = models.IntegerField(_('driving conditions'), choices=CONDITIONS_CHOICES)

    class Meta:
        app_label = "kx"
        ordering = ('-created_at',)


class TireBrandImagesThumbnail(models.Model):
    brand_name = models.CharField(max_length=155)
    size = models.CharField(max_length=50)
    path = models.CharField(max_length=1000)

    class Meta:
        app_label = "kx"
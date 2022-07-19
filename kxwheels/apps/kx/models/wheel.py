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


class ManufacturerManager(models.Manager):
    def get_query_set(self):
        return super(ManufacturerManager, self).get_query_set().order_by('name')

    def visible(self):
        hidden_manufacturers = None
        request = CrequestMiddleware.get_request()
        subdomain, subdomain_profile = extract_subdomain(request)
        if subdomain and subdomain_profile:
            user = subdomain_profile.user
            hidden_manufacturers = WheelManufacturerDiscount.objects.filter(
                user=user,
                is_visible=False
            ).values('manufacturer')

        if hidden_manufacturers:
            return self.filter(~Q(pk__in=hidden_manufacturers))
        else:
            return self.all()


class WheelManufacturer(StandardModel):
    name = models.CharField(_('name'), max_length=200)
    slug = models.SlugField(_('slug'), max_length=255, blank=True)
    description = models.TextField(_('description'), blank=True)
    is_configurator = models.BooleanField(_('is configurator available'), default=False, blank=True)
    picture = ImageField(_('picture'), upload_to='media/manufacturers',
                         blank=True, null=True)
    warranty = models.TextField(_('warranty'), blank=True, null=True)

    objects = ManufacturerManager()

    class Meta:
        app_label = "kx"
        ordering = ('name',)
        verbose_name = _('wheel manufacturer')
        verbose_name_plural = _('wheel manufacturers')

    def __unicode__(self):
        return unicode(self.name)

    @models.permalink
    def get_absolute_url(self):
        return ('wheel_wheel_list', [self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, instance=self)
        super(WheelManufacturer, self).save(*args, **kwargs)

class FeaturedBrand(StandardModel):
    name = models.CharField(_('name'), max_length=200)
    slug = models.SlugField(_('slug'), max_length=255, blank=True)
    description = models.TextField(_('description'), blank=True)
    is_configurator = models.BooleanField(_('is configurator available'), default=False, blank=True)
    picture = ImageField(_('picture'), upload_to='media/manufacturers',
                         blank=True, null=True)
    warranty = models.TextField(_('warranty'), blank=True, null=True)

    objects = ManufacturerManager()

    class Meta:
        app_label = "kx"
        ordering = ('name',)
        verbose_name = _('Featured Brand')
        verbose_name_plural = _('Featured Brands')

    def __unicode__(self):
        return unicode(self.name)

    @models.permalink
    def get_absolute_url(self):
        return ('wheel_wheel_list', [self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, instance=self)
        super(FeaturedBrand, self).save(*args, **kwargs)


class WheelManufacturerDiscount(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'), related_name='wheel_discounts')
    manufacturer = models.ForeignKey(WheelManufacturer, verbose_name=_('manufacturer'), related_name='discounts')
    discount = models.IntegerField(_('discount'), default=13)
    is_visible = models.BooleanField(_('Is this brand visible to dealer?'), default=True)

    def __unicode__(self):
        return "%s - %s%%" % (self.manufacturer, self.discount)

    class Meta:
        app_label = "kx"
        verbose_name = _('wheel manufacturer discount')
        verbose_name_plural = _('wheel manufacturer discounts')


class DealerWheelManufacturerDiscount(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'), related_name='dealer_wheel_discounts')
    manufacturer = models.ForeignKey(WheelManufacturer, verbose_name=_('manufacturer'), related_name='dealer_discounts')
    discount = models.IntegerField(_('discount'), default=25)

    def __unicode__(self):
        return "%s - %s%%" % (self.manufacturer, self.discount)

    class Meta:
        app_label = "kx"
        verbose_name = _('dealer wheel manufacturer discount')
        verbose_name_plural = _('dealer wheel manufacturer discounts')


class Wheel(StandardModel):
    manufacturer = models.ForeignKey(WheelManufacturer, verbose_name=_('manufacturer'), related_name='wheels')
    name = models.CharField(_('name'), max_length=200)
    slug = models.SlugField(_('slug'), max_length=255, blank=True)
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        app_label = "kx"
        ordering = ['name']
        verbose_name = _('wheel')
        verbose_name_plural = _('wheels')
        # unique_together = ('manufacturer', 'name')

    def __unicode__(self):
        return unicode(self.name)

    @models.permalink
    def get_absolute_url(self):
        return ('wheel_wheel_detail', [self.manufacturer.slug, self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_uuid(self.name)
        super(Wheel, self).save(*args, **kwargs)

    def get_num_reviews(self):
        return WheelReview.objects.filter(reviewee=self).count()

    def get_average_review(self):
        return WheelReview.objects.filter(reviewee=self).aggregate(Avg('rating'))['rating__avg'] or -1

    @property
    def thumbnail(self):
        try:
            result = self.pictures.all()[0].picture
        except IndexError:
            result = None
        return result


class WheelCoupon(models.Model):
    wheel = models.ForeignKey(Wheel, related_name='coupons')
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


class WheelCustomerMedia(models.Model):
    user = models.ForeignKey(User, verbose_name=_("uploader"), related_name="wheel_media", )
    wheel = models.ForeignKey(Wheel, related_name='customer_media', )
    title = models.CharField(_('title'), max_length=100)
    make = models.CharField(_('make'), max_length=255)
    year = models.CharField(_('year'), max_length=255)
    model = models.CharField(_('model'), max_length=255)
    picture = ImageField(_('picture'), upload_to='media/customer', help_text="Max size is 250 KiB", blank=True,
                         null=True)
    video = models.URLField(_('video'), max_length=255, help_text="YouTube Video URL", blank=True, null=True)
    comment = models.TextField(_('comments'), max_length=500, blank=True, null=True)

    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    objects = models.Manager()
    active = ActiveCustomerMediaManager()

    class Meta:
        app_label = "kx"


class WheelSize(HardProduct):
    AVAILABILITY_CHOICES = (
        (0, 'Manufacturer Direct'),
        (1, 'Ships in 1-2 Weeks'),
        (2, 'ETA 2-4 Weeks'),
        (3, 'Custom Build'),
        (4, 'Specialty Order'),
        (5, 'Call for Availability'),
    )

    wheel = models.ForeignKey(Wheel, verbose_name=_('wheel'), related_name='sizes')
    wheelwidth = models.DecimalField(_('wheel width'), max_digits=4, decimal_places=1,
                                     blank=True, null=True, db_index=True)
    diameter = models.DecimalField(_("diameter"), max_digits=4,
                                   decimal_places=1, blank=True, null=True, db_index=True)
    offset = models.IntegerField(_('offset'), blank=True, null=True, db_index=True)
    finish = models.CharField(_('finish'), max_length=50, blank=True, null=True, db_index=True)
    boltpattern_1 = models.CharField(_('boltpattern 1'), max_length=20, blank=True, null=True, default=0, db_index=True)
    boltpattern_2 = models.CharField(_('boltpattern 2'), max_length=20, blank=True, null=True, default=0, db_index=True)
    centerbore = models.CharField(_('centerbore'), max_length=10, blank=True, null=True)
    availability = models.IntegerField("Availability", choices=AVAILABILITY_CHOICES,
                                       blank=True, null=True, db_index=True)

    def get_thumbnail_med(self):
        try:
            thumbnail = self.wheel.pictures.all()[0].thumbnails.filter(size="med")[0].path
        except:
            thumbnail = None
        return thumbnail

    class Meta:
        app_label = "kx"
        ordering = ("diameter",)
        verbose_name = _('wheel size')
        verbose_name_plural = _('wheel sizes')
        unique_together = ('wheel', 'sku')

    def __unicode__(self):
        return "%s (%s x %s)" % (self.wheel.name, self.diameter, self.wheelwidth)

    @models.permalink
    def get_absolute_url(self):
        return ('wheel_wheelsize_detail', [self.wheel.manufacturer.slug,
                                           self.wheel.slug,
                                           self.sku])

    def save(self, *args, **kwargs):
        '''
        if self.pk and not self.sku:
            self.sku = 'W%s' % str(self.pk).zfill(10)
        '''
        if not self.short_desc:
            self.short_desc = "No description available"
        if not self.long_desc:
            self.long_desc = "No description available"
        if not self.name:
            self.name = "%s %s %s x %s (%smm) %s %s" % (
                self.wheel.manufacturer.name,
                self.wheel.name,
                self.get_diameter(),
                self.get_wheelwidth(),
                self.offset,
                self.boltpattern_1,
                self.boltpattern_2
            )
        super(WheelSize, self).save(*args, **kwargs)

    def get_diameter(self):
        # return self.diameter
        return cut_decimals(self.diameter)

    def get_wheelwidth(self):
        # return self.wheelwidth
        return cut_decimals(self.wheelwidth)

    def get_price(self, user=None, subdomain=None):
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
                    markup = DealerWheelManufacturerDiscount.objects.get(
                        manufacturer=self.wheel.manufacturer,
                        user=subdomain_profile.user,
                    ).discount
        except:
            pass
        try:
            if subdomain:
                discount = WheelManufacturerDiscount.objects.get(
                    manufacturer=self.wheel.manufacturer,
                    user=subdomain_profile.user,
                ).discount
        except:
            pass

        price = str(round((self.price * (100 - discount) / 100 * (100 + markup) / 100) * 2, 1) / 2)
        return price

    @property
    def thumbnail(self):
        try:
            result = self.wheel.pictures.all()[0].picture
        except IndexError:
            result = None
        return result


class WheelPicture(models.Model):
    wheel = models.ForeignKey(Wheel, verbose_name=_('wheel'), related_name="pictures")
    picture = ImageField(_('picture'), upload_to='media/wheels',
                         blank=True, null=True)
    caption = models.CharField(_('optional caption'), max_length=255, null=True, blank=True)

    class Meta:
        app_label = "kx"
        verbose_name = _('wheel picture')
        verbose_name_plural = _('wheel pictures')

    def save(self, *args, **kwargs):
        super(WheelPicture, self).save(*args, **kwargs)

        # Generate thumbnails
        try:
            # - Large
            url = get_thumbnail(self.picture, '275x275').url
            thumbnail, created = WheelPictureThumbnail.objects.get_or_create(
                wheelpicture=self,
                size="lg",
            )
            url = urlparse(url)
            path = "{0}://{1}{2}".format(url.scheme, url.netloc, url.path)
            thumbnail.path = path
            thumbnail.save()

            # - Medium
            url = get_thumbnail(self.picture, '140x140').url
            thumbnail, created = WheelPictureThumbnail.objects.get_or_create(
                wheelpicture=self,
                size="med",
            )
            url = urlparse(url)
            path = "{0}://{1}{2}".format(url.scheme, url.netloc, url.path)
            thumbnail.path = path
            thumbnail.save()

            # - Small
            url = get_thumbnail(self.picture, '80x80').url
            thumbnail, created = WheelPictureThumbnail.objects.get_or_create(
                wheelpicture=self,
                size="sm",
            )
            url = urlparse(url)
            path = "{0}://{1}{2}".format(url.scheme, url.netloc, url.path)
            thumbnail.path = path
            thumbnail.save()
        except IOError, e:
            pass
            # TODO: Handle thumbnail creation failure properly


class WheelPictureThumbnail(models.Model):
    wheelpicture = models.ForeignKey(WheelPicture, related_name="thumbnails")
    size = models.CharField(max_length=50)
    path = models.CharField(max_length=1000)

    class Meta:
        app_label = "kx"


class WheelReview(BaseReview):
    reviewee = models.ForeignKey(Wheel, verbose_name=_('reviewee'), related_name="reviews", )
    reviewer = models.ForeignKey(User, verbose_name=_("reviewer"),
                                 related_name="wheel_reviews", blank=True, null=True)
    make = models.CharField(_('make'), max_length=255)
    year = models.CharField(_('year'), max_length=255)
    model = models.CharField(_('model'), max_length=255)
    mileage = models.IntegerField(_('mileage'), blank=True, null=True,
                                  help_text=_('Distance travelled on wheels'))

    def __unicode__(self):
        return unicode(self.reviewee)

    class Meta:
        app_label = "kx"
        ordering = ('-created_at',)


class WheelScrappedPictures(models.Model):
    part_no = models.CharField(_('part_no'), max_length=255)
    part_no = models.CharField(_('part_no'), max_length=255)
    pic_url = models.CharField(_('pic_url'), max_length=255)

    def __unicode__(self):
        return unicode(self.part_no)


class WheelSliderImages(models.Model):
    image = ImageField(_('image'), upload_to='static/img/slides/',
                             blank=True, null=True)
    image_link = models.CharField(_('image_link'), max_length=255, null=True, blank=True)
    part_no = models.CharField(_('part_no'), max_length=255, blank=True, null=True)

    class Meta:
        app_label = "kx"
        verbose_name = _('wheel sliderimages')
        verbose_name_plural = _('wheel sliderimagess')

    def save(self, *args, **kwargs):
        super(WheelSliderImages, self).save(*args, **kwargs)

        try:
            # - Large
            url = get_thumbnail(self.image, '940x330').url
            thumbnail, created = WheelSliderImagesThumbnail.objects.get_or_create(
                WheelSliderImages=self,
                size="lg",
            )
            url = urlparse(url)
            path = "{0}://{1}{2}".format(url.scheme, url.netloc, url.path)
            thumbnail.path = path
            thumbnail.save()
        except IOError, e:
            pass
            # TODO: Handle thumbnail creation failure properly

class WheelSliderImagesThumbnail(models.Model):
    WheelSliderImages = models.ForeignKey(WheelSliderImages, related_name="thumbnails")
    size = models.CharField(max_length=50)
    path = models.CharField(max_length=1000)

    class Meta:
        app_label = "kx"


class WheelBrandImagesThumbnail(models.Model):
    brand_name = models.CharField(max_length=155)
    size = models.CharField(max_length=50)
    path = models.CharField(max_length=1000)

    class Meta:
        app_label = "kx"

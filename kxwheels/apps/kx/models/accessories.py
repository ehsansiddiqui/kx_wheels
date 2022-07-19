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


class Accessories(StandardModel):
    name = models.CharField(_('name'), max_length=200)
    slug = models.SlugField(_('slug'), max_length=255, blank=True)
    description = models.TextField(_('description'), blank=True)
    is_configurator = models.BooleanField(_('is configurator available'), default=False, blank=True)
    picture = ImageField(_('picture'), upload_to='media/accessories_logos',
                         blank=True, null=True)
    warranty = models.TextField(_('warranty'), blank=True, null=True)

    class Meta:
        app_label = "kx"
        ordering = ('name',)
        verbose_name = _('accessories')
        verbose_name_plural = _('accessories')

    def __unicode__(self):
        return unicode(self.name)

    @models.permalink
    def get_absolute_url(self):
        return ('accessories_list', [self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, instance=self)
        super(Accessories, self).save(*args, **kwargs)


class AccessoriesList(StandardModel):
    manufacturer = models.ForeignKey(Accessories, verbose_name=_('accessories'), related_name='accessories')
    name = models.CharField(_('name'), max_length=200)
    slug = models.SlugField(_('slug'), max_length=255, blank=True)
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        app_label = "kx"
        ordering = ['name']
        verbose_name = _('accessories list')
        verbose_name_plural = _('accessories list')

    def __unicode__(self):
        return unicode(self.name)

    @models.permalink
    def get_absolute_url(self):
            return ('accessories_detail', [self.manufacturer.slug, self.slug])

    @property
    def thumbnail(self):
        try:
            result = self.pictures.all()[0].picture
        except IndexError:
            result = None
        return result


class AccessoriesPicture(models.Model):
    wheel = models.ForeignKey(AccessoriesList, verbose_name=_('accessories_list'), related_name="pictures")
    picture = ImageField(_('picture'), upload_to='media/accessories',
                         blank=True, null=True)
    caption = models.CharField(_('optional caption'), max_length=255, null=True, blank=True)

    class Meta:
        app_label = "kx"
        verbose_name = _('accessorie picture')
        verbose_name_plural = _('accessorie pictures')

    def save(self, *args, **kwargs):
        super(AccessoriesPicture, self).save(*args, **kwargs)

        # Generate thumbnails
        try:
            # - Large
            url = get_thumbnail(self.picture, '275x275').url
            thumbnail, created = AccessoriesPictureThumbnail.objects.get_or_create(
                wheelpicture=self,
                size="lg",
            )
            url = urlparse(url)
            path = "{0}://{1}{2}".format(url.scheme, url.netloc, url.path)
            thumbnail.path = path
            thumbnail.save()

            # - Medium
            url = get_thumbnail(self.picture, '140x140').url
            thumbnail, created = AccessoriesPictureThumbnail.objects.get_or_create(
                wheelpicture=self,
                size="med",
            )
            url = urlparse(url)
            path = "{0}://{1}{2}".format(url.scheme, url.netloc, url.path)
            thumbnail.path = path
            thumbnail.save()

            # - Small
            url = get_thumbnail(self.picture, '80x80').url
            thumbnail, created = AccessoriesPictureThumbnail.objects.get_or_create(
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


class AccessoriesCoupon(models.Model):
    wheel = models.ForeignKey(AccessoriesList, related_name='coupons')
    picture = ImageField(_('picture'), upload_to='media/accessories_coupons', )
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


class AccessoriesCustomerMedia(models.Model):
    user = models.ForeignKey(User, verbose_name=_("uploader"), related_name="accessorie_media", )
    accessorie = models.ForeignKey(AccessoriesList, related_name='customer_media', )
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


class AccessoriesReview(BaseReview):
    reviewee = models.ForeignKey(AccessoriesList, verbose_name=_('reviewee'), related_name="reviews", )
    reviewer = models.ForeignKey(User, verbose_name=_("reviewer"),
                                 related_name="accessories_reviews", blank=True, null=True)
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


class AccessoriesDiscount(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'), related_name='accesories_discounts')
    accesories = models.ForeignKey(Accessories, verbose_name=_('accesories'), related_name='discounts')
    discount = models.IntegerField(_('discount'), default=13)
    is_visible = models.BooleanField(_('Is this brand visible to dealer?'), default=True)

    def __unicode__(self):
        return "%s - %s%%" % (self.accesories, self.discount)

    class Meta:
        app_label = "kx"
        verbose_name = _('wheel accesories discount')
        verbose_name_plural = _('wheel accesories discounts')


class DealerAccessoriesDiscount(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'), related_name='dealer_accesories_discounts')
    accessories = models.ForeignKey(Accessories, verbose_name=_('manufacturer'), related_name='dealer_discounts')
    discount = models.IntegerField(_('discount'), default=25)

    def __unicode__(self):
        return "%s - %s%%" % (self.accessories, self.discount)

    class Meta:
        app_label = "kx"
        verbose_name = _('dealer accessories discount')
        verbose_name_plural = _('dealer accessories discounts')


class AccessoriesDetail(HardProduct):

    accessories_list = models.ForeignKey(AccessoriesList, verbose_name=_('accessories list'), related_name='sizes')
    accessoriewidth = models.DecimalField(_('wheel width'), max_digits=4, decimal_places=1,
                                     blank=True, null=True, db_index=True)
    diameter = models.DecimalField(_("diameter"), max_digits=4,
                                   decimal_places=1, blank=True, null=True, db_index=True)
    offset = models.IntegerField(_('offset'), blank=True, null=True, db_index=True)
    finish = models.CharField(_('finish'), max_length=50, blank=True, null=True, db_index=True)

    def get_thumbnail_med(self):
        try:
            thumbnail = self.accessories_list.pictures.all()[0].thumbnails.filter(size="med")[0].path
        except:
            thumbnail = None
        return thumbnail

    class Meta:
        app_label = "kx"
        ordering = ("diameter",)
        verbose_name = _('accessorie detail')
        verbose_name_plural = _('accessorie details')
        # unique_together = ('wheel', 'sku')

    def __unicode__(self):
        return "%s (%s x %s)" % (self.accessories_list.name, self.diameter, self.accessoriewidth)

    @models.permalink
    def get_absolute_url(self):
        return ('accessories_detail', [self.accessories_list.manufacturer.slug,
                                           self.accessories_list.slug,
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
            self.name = "%s %s %s x %s " % (
                self.accessories_list.manufacturer.name,
                self.accessories_list.name,
                self.get_diameter(),
                self.get_wheelwidth()
            )
        super(AccessoriesDetail, self).save(*args, **kwargs)

    def get_diameter(self):
        # return self.diameter
        return cut_decimals(self.diameter)

    def get_wheelwidth(self):
        # return self.wheelwidth
        return cut_decimals(self.accessoriewidth)

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
                    markup = DealerAccessoriesDiscount.objects.get(
                        accessories=self.accessories_list.accessories,
                        user=subdomain_profile.user,
                    ).discount
        except:
            pass
        try:
            if subdomain:
                discount = AccessoriesDiscount.objects.get(
                    accessories=self.accessories_list.accessories,
                    user=subdomain_profile.user,
                ).discount
        except:
            pass

        price = str(round((self.price * (100 - discount) / 100 * (100 + markup) / 100) * 2, 1) / 2)
        return price

    @property
    def thumbnail(self):
        try:
            result = self.accessories_list.pictures.all()[0].picture
        except IndexError:
            result = None
        return result


class AccessoriesPictureThumbnail(models.Model):
    wheelpicture = models.ForeignKey(AccessoriesPicture, related_name="thumbnails")
    size = models.CharField(max_length=50)
    path = models.CharField(max_length=1000)

    class Meta:
        app_label = "kx"

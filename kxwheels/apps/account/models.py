from uuid import uuid4
from hashlib import sha256

from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

class Profile(models.Model):
    user = models.ForeignKey(User, verbose_name=_("customer"), related_name="profiles", blank=True,)
    site = models.ForeignKey(Site, verbose_name=_("site"), related_name="profiles", blank=True, null=True)
    name = models.CharField(_("profile name"), help_text=_('Personal, Work, etc'), max_length=255)

    first_name = models.CharField(_("first name"), max_length=255,)
    last_name = models.CharField(_("last name"), max_length=255,)
    landline_phone = models.CharField(_("landline phone"), max_length=16,)
    cell_phone = models.CharField(_("cell phone"), max_length=16, blank=True, null=True )
    fax = models.CharField(_("fax"), max_length=16, blank=True, null=True)

    address_1 = models.CharField(_("address 1"), max_length=255, blank=True)
    address_2 = models.CharField(_("address 2"), max_length=255, blank=True)
    city = models.CharField(_("city"), max_length=255, blank=True)
    postal_code = models.CharField(_("postal/zip code"), max_length=20, blank=True)
    province = models.CharField(_("province"), max_length=255, blank=True)
    country = models.CharField(_("country"), max_length=255, blank=True)

    subdomain = models.CharField(_("subdomain"), max_length=50, blank=True, null=True, unique=True)

    dealer_logo = models.ImageField(_("dealer_logo"), upload_to='media/dealer_logo', blank=True, null=True)
    banner = models.ImageField(_("banner"), upload_to='media/banner', blank=True, null=True)

    class Meta:
        unique_together = ('user', 'name',)

    @models.permalink
    def get_absolute_url(self):
        return ('auth_profile_detail', [self.name])

    def get_full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        if not self.subdomain:
            self.subdomain = None
        super(Profile, self).save(*args, **kwargs)

class Developer(models.Model):
    user = models.OneToOneField(User, verbose_name=_("developer"), related_name="developer_profile", blank=True,)
    site = models.ForeignKey(Site, verbose_name=_("site"), related_name="developer_profile", blank=True)
    access_key = models.CharField(max_length=32, blank=True)
    secret_key = models.CharField(max_length=64, blank=True)

    is_active = models.BooleanField()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.access_key = uuid4().hex.upper()
            self.secret_key = sha256(uuid4().hex).hexdigest().upper()
        super(Developer, self).save(*args, **kwargs)

class Dealer(models.Model):
    BUSINESS_KINDS = (
        (1, 'Tire shop'),
        (2, 'Custom wheel shop'),
        (3, 'Online business'),
        (4, 'Other'),
    )

    business_name = models.CharField(_("business name"), max_length=255)
    contact_name = models.CharField(_("contact name"), max_length=255)

    street_address = models.CharField(_("streeet address"), max_length=255, blank=True)
    city = models.CharField(_("city"), max_length=255, blank=True)
    postal_code = models.CharField(_("postal/zip code"), max_length=20, blank=True)
    province = models.CharField(_("province"), max_length=255, blank=True)
    country = models.CharField(_("country"), max_length=255, blank=True)

    email = models.EmailField(_("email"), max_length=255)
    business_phone = models.CharField(_("business phone"), max_length=20)
    other_phone = models.CharField(_("other phone"), max_length=20, blank=True, null=True)

    heard = models.TextField(_("where did you hear about us?"), max_length=500)
    business_kind = models.IntegerField(_("what kind of business do you have?"), choices=BUSINESS_KINDS)
    business_kind_other = models.CharField(_("business other"), max_length=500, blank=True, null=True)
    interested_in = models.TextField(_("what products are you interested in?"), max_length=500)
    volume = models.TextField(_("What do you expect your monthly volume to be?"), max_length=500)
    comments = models.TextField(_("comments"), max_length=500)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    def __unicode__(self):
        return self.business_name

from kxwheels.apps.account import listeners
listeners.start_listening()


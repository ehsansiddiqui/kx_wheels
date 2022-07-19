from django.db import models
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail import ImageField
from sorl.thumbnail.shortcuts import get_thumbnail

class StandardModelManager(models.Manager):
    def active(self, **kwargs):
        return self.filter(is_active=True, **kwargs)



class StandardModel(models.Model):
    meta_title = models.CharField(_('meta title'), max_length=255, blank=True, null=True)
    meta_keywords = models.CharField(_('meta keywords'), max_length=255, blank=True, null=True)
    meta_description = models.CharField(_('meta description'), max_length=500, blank=True, null=True)
    ordering = models.IntegerField(_('sort order'), blank=True, null=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True, blank=True, null=True)
    is_active = models.BooleanField(_('is active?'), default=1)

    objects = StandardModelManager()

    class Meta:
        abstract = True



class ManufacturerManager(models.Manager):
    def visible(self, user):
        hidden_manufacturers = None
        if user.is_authenticated() and user.is_active:
            hidden_manufacturers = ManufacturerDiscount.objects.filter(
                user=user,
                is_visible=False
            ).values('manufacturer')

        if hidden_manufacturers:
            return self.filter(~Q(pk__in=hidden_manufacturers))
        else:
            return self.all()



class Task(models.Model):
    task = models.CharField(primary_key=True, max_length=255)
    session = models.CharField(max_length=255)
    is_completed = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __unicode__(self):
        return self.task

    class Meta:
        app_label = "kx"



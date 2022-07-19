from django.db import models
from django.utils.translation import ugettext_lazy as _

from kxwheels.apps.reviews.conf import settings

class ApprovedReviewManager(models.Manager):
    def get_query_set(self):
        return super(ApprovedReviewManager, self).get_query_set().filter(is_approved=True)


class BaseReview(models.Model):
    title = models.CharField(_('title of your review'), max_length=255, help_text=_("e.g, A great product."))
    name = models.CharField(_('your name'), max_length=255, blank=True)
    rating = models.PositiveIntegerField(_('rating'), choices=settings.RATING_CHOICES)

    
    buy_again = models.IntegerField(_('would buy again?'),
                                    choices=settings.BUY_AGAIN_CHOICES)
    recommend = models.IntegerField(_('would recommend?'),
                                    choices=settings.RECOMMEND_CHOICES)

    # Comments
    pros = models.TextField(_('pros'), help_text=_('What do you think is good about this produt.'))
    cons = models.TextField(_('cons'), help_text=_('What do you think is not-so-good about this product.'))
    bottom_line = models.TextField(_('bottom line'), blank=True, null=True,
                                   help_text=_('All things considered, how would you conclude.'))

    # Audit
    ip = models.GenericIPAddressField(_('IP address'), blank=True, null=True)
    created_at = models.DateTimeField(_('created at'),
                                      auto_now_add=True,
                                      blank=True)

    # Moderation
    is_approved = models.BooleanField(default=False)
    upvotes = models.IntegerField(_('up votes'), default=0, blank=True, null=True)
    downvotes = models.IntegerField(_('down votes'), default=0, blank=True, null=True)

    objects = models.Manager()
    approved = ApprovedReviewManager()

    class Meta:
        abstract = True

    @property
    def netvotes(self):
        return self.upvotes - self.downvotes

    

    
    

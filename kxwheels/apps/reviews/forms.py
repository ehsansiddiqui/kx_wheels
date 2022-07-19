from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_unicode, force_unicode

from kxwheels.apps.reviews.conf import settings
from kxwheels.apps.reviews.models import BaseReview
from recaptcha.client import captcha

class RatingInput(forms.widgets.RadioSelect):
    def tag(self):
        if 'id' in self.attrs:
            self.attrs['id'] = '%s_%s' % (self.attrs['id'], self.index)
        final_attrs = dict(self.attrs, type='radio', name=self.name, value=self.choice_value)
        if self.is_checked():
            final_attrs['checked'] = 'checked'
        # Add title here
        final_attrs['title'] = self.choice_label
        return mark_safe(u'<input%s />' % forms.util.flatatt(final_attrs))

class RatingWidgetRenderer(forms.widgets.RadioFieldRenderer):
    def __iter__(self):
        for i, choice in enumerate(self.choices):
            yield RatingInput(self.name, self.value, self.attrs.copy(), choice, i)

    def __getitem__(self, idx):
        choice = self.choices[idx] # Let the IndexError propogate
        return RatingInput(self.name, self.value, self.attrs.copy(), choice, idx)

    def render(self):
        """Outputs a <ul> for this set of radio fields."""
        var_msg = "%s_msg" % self.name
        return mark_safe(u'<ul>\n%s\n</ul><span id="%s"></span>'
            % (u'\n'.join([u'<li>%s</li>' % force_unicode(w) for w in self]), var_msg))

class ReCaptchaWidget(forms.widgets.Widget):
    recaptcha_challenge_name = 'recaptcha_challenge_field'
    recaptcha_response_name = 'recaptcha_response_field'

    def render(self, name, value, attrs=None):
        return mark_safe(u'%s' % captcha.displayhtml(settings.RECAPTCHA_PUBLIC_KEY))

    def value_from_datadict(self, data, files, name):
        return [data.get(self.recaptcha_challenge_name, None),
                data.get(self.recaptcha_response_name, None)]


class ReCaptchaField(forms.CharField):
    default_error_messages = {
        'captcha_invalid': _(u'Invalid captcha')
    }

    def __init__(self, *args, **kwargs):
        self.widget = ReCaptchaWidget
        self.required = True
        super(ReCaptchaField, self).__init__(*args, **kwargs)

    def clean(self, values):
        super(ReCaptchaField, self).clean(values[1])
        recaptcha_challenge_value = smart_unicode(values[0])
        recaptcha_response_value = smart_unicode(values[1])
        check_captcha = captcha.submit(recaptcha_challenge_value,
            recaptcha_response_value, settings.RECAPTCHA_PRIVATE_KEY, {})
        if not check_captcha.is_valid:
            raise forms.util.ValidationError(self.error_messages['captcha_invalid'])
        return values[0]



class BaseReviewForm(forms.ModelForm):
    rating = forms.IntegerField(label=_('Rating'), min_value=1, max_value=5,
                                widget=forms.RadioSelect(renderer=RatingWidgetRenderer,
                                                         choices=settings.RATING_CHOICES))

    upvotes = forms.IntegerField(widget=forms.HiddenInput, required=False)
    downvotes = forms.IntegerField(widget=forms.HiddenInput, required=False)
    recaptcha = ReCaptchaField(label=_('Verification'), help_text=_('Please enter the code into the box'))

    def __init__(self, *args, **kwargs):
        super(BaseReviewForm, self).__init__(*args, **kwargs)

        for field in self.fields.items():
            self.fields[field[0]].label = mark_safe("{0}<span>{1}</span>".format(
                unicode(self.fields[field[0]].label),
                unicode(self.fields[field[0]].help_text)
            ))

            if isinstance(field[1], forms.CharField) or \
               isinstance(field[1], forms.IntegerField):
                self.fields[field[0]].widget.attrs['class'] = 'textInput'

    class Meta:
        model = BaseReview
        exclude = ('is_approved',)

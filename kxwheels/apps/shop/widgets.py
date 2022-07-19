from django import forms
from django.utils.encoding import force_unicode
from django.utils.html import escape, conditional_escape

class InterestingInput(forms.SelectMultiple):

    def render_option(self, selected_choices, option_value, option_label):
        option_value = force_unicode(option_value)
        selected_html = (option_value in selected_choices) and u' selected="selected"' or ''
        return u'<option value="%s"%s>%s</option>' % (
            escape(option_value), selected_html,
            conditional_escape(force_unicode(option_label)))


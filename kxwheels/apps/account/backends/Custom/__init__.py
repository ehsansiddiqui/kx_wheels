from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.contrib.sites.models import RequestSite, Site

from registration import signals
from registration.forms import RegistrationForm
from registration.models import RegistrationProfile

from kxwheels.apps.account import signals as account_signals


class CustomBackend(object):
    def register(self, request, **kwargs):
        username, email, password = kwargs['username'], kwargs['email'], kwargs['password1']
        first_name, last_name = kwargs['first_name'], kwargs['last_name']

        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)

        new_user = RegistrationProfile.objects.create_inactive_user(
            username, email, password, site)

        new_user.email= email
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.is_active = True
        new_user.save()

        auth_new_user = authenticate(email=new_user.email,
                                     password=request.POST['password1'])
        login(request, auth_new_user)

        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)

        return new_user

    def profile(self, request, **kwargs):
        """docstring for profile"""
        pass

    def activate(self, request, activation_key):
        activated = RegistrationProfile.objects.activate_user(activation_key)
        if activated:
            signals.user_activated.send(sender=self.__class__,
                                        user=activated,
                                        request=request)
        return activated

    def registration_allowed(self, request):
        return getattr(settings, 'REGISTRATION_OPEN', True)

    def get_form_class(self, request):
        return RegistrationForm

    def post_registration_redirect(self, request, user):
        next = request.GET.get('next', None)
        if next is not None:
            return (next, (), {})
        else:
            return ('registration_complete', (), {})

    def post_activation_redirect(self, request, user):
        return ('registration_activation_complete', (), {})


class EmailBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        try:
            validate_email(username)
        except ValidationError:
            return None
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        return None
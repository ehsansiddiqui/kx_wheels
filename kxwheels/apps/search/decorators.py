from kxwheels.apps.account.models import Developer
from django.http import HttpResponseForbidden
from django.core.context_processors import csrf

try:
    from functools import update_wrapper, wraps
except ImportError:
    from django.utils.functional import update_wrapper, wraps


def csrf_token_required(view_func):
    def _decorated(self, *args, **kwargs):
        request = self.request
        user_token = request.GET.get('csrfmiddlewaretoken', None) or request.POST.get('csrfmiddlewaretoken', None)
        server_token = csrf(self.request)['csrf_token']

        if user_token:
            if user_token == server_token:
                return view_func(self, *args, **kwargs)
        return HttpResponseForbidden('CSRF Failed')
    return _decorated

def api_access_required(view_func):
    # type: (object) -> object
    def _decorated(self, *args, **kwargs):
        request = self.request
        access_key = request.GET.get('access_key', None) or request.POST.get('access_key', None)
        # Just identification no authentication or authorization
        if access_key:
            try:
                developer = Developer.objects.get(access_key=access_key)
            except Developer.DoesNotExist, e:
                pass
            else:
                if developer.is_active:
                    return view_func(self, *args, **kwargs)
        return HttpResponseForbidden('API Access Failed')
    return _decorated

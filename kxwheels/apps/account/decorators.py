from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied
try:
    from functools import update_wrapper, wraps
except ImportError:
    from django.utils.functional import update_wrapper, wraps

def require_superuser(function):
    def _inner(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied           
        return function(request, *args, **kwargs)
    return _inner

def require_owner(model=None,):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            grant = False
            if model and 'object_id' in kwargs:
                object_id = kwargs.get('object_id')
                if object_id is not None:
                    if model.objects.get(pk=object_id).user == request.user:
                        grant = True
                    else:
                        grant = False
            if grant:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("Error 403: Request forbidden.")
        return wraps(view_func)(_wrapped_view)
    return decorator

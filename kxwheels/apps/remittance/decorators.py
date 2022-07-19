from django.core.cache import cache
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
try:
    from functools import update_wrapper, wraps
except ImportError:
    from django.utils.functional import update_wrapper, wraps

def require_gateway(view_func):
    def _decorated(request, *args, **kwargs):
        # Set return path in request object
        default_return_path = request.META.get('HTTP_REFERER', '/')
        return_path = request.POST.get('return_path', default_return_path)
        setattr(request, "return_path", return_path)
        
        # Check to see if the gateway is in cache

        #gateway = cache.get(kwargs.get('cache_key', None), None)
        gateway = request.session.get('gateway', None)
        if gateway is None:
            messages.add_message(request, messages.ERROR, 
                _('Payment gateway not found.'))
            return HttpResponseRedirect(reverse('remittance_payment_failure'))

        '''
        setattr(request, "gateway", gateway)
        '''
        return view_func(request, *args, **kwargs)
    return _decorated

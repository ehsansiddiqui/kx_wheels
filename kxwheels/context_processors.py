from django.conf import settings
from django.contrib.auth.models import User

from apps.account.models import Profile
from kxwheels.apps.vehicle.models import Model


def get_subdomain_owner(request):
    domain_info = extract_subdomain(request)
    if not domain_info['subdomain']: return None

    subdomain_owners = User.objects.filter(
        profiles__subdomain=domain_info['subdomain'],
        profiles__subdomain__isnull=False
    )
    if len(subdomain_owners):
        return subdomain_owners[0]
    else:
        return None


def extract_subdomain(request):
    subdomain = None
    url = None
    subdomain_profile = None
    host = request.META.get('HTTP_HOST', '')
    host_s = host.replace('www.', '').split('.')
    if len(host_s) > 2:
        subdomain = ''.join(host_s[:-2])
        if host_s[-2] != 'wheels-canada':
            url = host[len(subdomain) + 1:]
            subdomain = 'www'
        else:
            try:
                subdomain_profile = Profile.objects.get(subdomain=subdomain)
            except:
                url = host[len(subdomain) + 1:]
                subdomain = "www"
    return {'subdomain': subdomain,
            'url': url,
            'subdomain_profile': subdomain_profile,
            'current_user': request.user}


def api_access_key(request):
    access_key = getattr(settings, 'API_ACCESS_KEY', None)
    return {'api_access_key': access_key}


def selected_vehicle(request):
    return {'selected_vehicle': Model.get_from_cache(request)}

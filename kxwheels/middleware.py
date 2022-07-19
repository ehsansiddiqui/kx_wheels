from django.conf import settings

class APIAccessKeyInjector(object):
    def process_request(self, request):
        access_key = getattr(settings, 'API_ACCESS_KEY', None)
        setattr(request, 'api_access_key', access_key)
        return None



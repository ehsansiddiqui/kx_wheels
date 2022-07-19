from .base import *

DEBUG = False
ALLOWED_HOSTS = ['.kxwheels.com', ]
STATIC_ROOT = '/media/kxwheels/assets/static'
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
MIDDLEWARE_CLASSES += ('rollbar.contrib.django.middleware.RollbarNotifierMiddleware', )
ROLLBAR['environment'] = 'production'
ADMIN_EMAIL = "info@kxwheels.com"

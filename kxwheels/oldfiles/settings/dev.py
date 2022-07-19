import djcelery
import os
import sys
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

from kxwheels.paypal_express_checkout.settings import *

djcelery.setup_loader()
rel = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)
sys.path.insert(0, rel("../apps"))

PROJECT_NAME = "project"


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'kxwheels',
        'USER': 'nav',
        'PASSWORD': '1mg01ng1n',
        'HOST': 'pg1.home.navaulakh.com',
        'PORT': '5432',
    }
}



TIME_ZONE = 'America/Vancouver'


#MEDIA_ROOT = rel('../../static/media')
#MEDIA_URL = '/static/media/'
MEDIA_URL = 'https://kxwheels.s3.amazonaws.com/'

#STATIC_URL = 'https://kxwheels.s3.amazonaws.com/static/'
STATIC_URL = '/static/'
STATICFILES_DIRS = (rel('../../static/assets'),)

# Change me
#ADMIN_MEDIA_ROOT = rel('../lib/python2.7/site-packages/django/contrib/admin/media/')
#ADMIN_MEDIA_PREFIX = '/static/media_admin/'
ADMIN_MEDIA_PREFIX = 'https://kxwheels.s3.amazonaws.com/static/admin/'


TEMPLATE_DIRS = (
    rel('../../static/templates'),
    rel('../apps/tire/templates'),
    rel('../apps/wheel/templates'),
    rel('../apps/vehicle/templates'),
    rel('../apps/accessories/templates'),
)


ROOT_URLCONF = 'project.urls'

AUTHENTICATION_BACKENDS = (
    "apps.account.backends.Custom.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",
)


MIDDLEWARE_CLASSES += (
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'project.middleware.APIAccessKeyInjector'
)


TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
    'project.context_processors.api_access_key',
)


INSTALLED_APPS += (
    'django.contrib.admin',
    'django.contrib.flatpages',
    'django.contrib.markup',

    'south',
    'haystack',
    'registration',
    'sorl.thumbnail',
    #'debug_toolbar',
    # 'kombu.transport.django',

    'account',
    'l10n',
    'shop',
    'search',
    'remittance',
    'shipping',

    'kx',
    'reviews',
    #'tire',
    #'wheel',
    'vehicle',
    #'accessories',
)


# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
#         },
#         'simple': {
#             'format': '%(levelname)s %(message)s'
#         },
#     },
#     'handlers': {
#         'mail_admins': {
#             'level': 'ERROR',
#             'class': 'django.utils.log.AdminEmailHandler'
#         },
#         'project': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'formatter': 'simple',
#             'filename': rel('../../logs/project.log'),
#         },
#         'import': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'formatter': 'simple',
#             'filename': rel('../../logs/import.log'),
#             },
#
#     },
#     'loggers': {
#         'django.request': {
#             'handlers': ['mail_admins',],
#             'level': 'ERROR',
#             'propagate': True,
#         },
#         'project.project': {
#             'handlers': ['project',],
#             'propagate': True,
#         },
#         'project.import': {
#             'handlers': ['import',],
#             'propagate': True,
#         },
#     }
# }


if not DEBUG:
    PREPEND_WWW = True


IGNORABLE_404_ENDS = ('favicon.ico', 'robots.txt',)
IGNORABLE_404_STARTS = ('',)
LOGIN_REDIRECT_URL = '/'


# Email
SERVER_EMAIL = "mailer@kxwheels.com"
DEFAULT_FROM_EMAIL = "KX Wheels <mailer@kxwheels.com>"
EMAIL_SUBJECT_PREFIX = "[KX Wheels] - "
EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
EMAIL_HOST_USER = 'AKIAINF5HHHP6QX42SQA'
EMAIL_HOST_PASSWORD = 'AtIVhIG97WxRL4JT5pGC1WlgBZ2+DKDbKkvHbyrxqnXr'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Haystack
HAYSTACK_SITECONF = 'search.sites'
HAYSTACK_SEARCH_ENGINE = 'solr'
HAYSTACK_SOLR_URL = 'http://localhost:8983/solr'

# South
SOUTH_TESTS_MIGRATE = False

# Sorl thumbnail
THUMBNAIL_DEBUG = False
THUMBNAIL_PREFIX = 'media/cache/'

# Debug toolbar
INTERCEPT_REDIRECTS = False
INTERNAL_IPS = ('127.0.0.1',)


# Recaptcha
RECAPTCHA_PUBLIC_KEY = '6LdLtMQSAAAAAMzOGkiFGuaaexpSLuagoqxoWZ1L'
RECAPTCHA_PRIVATE_KEY = '6LdLtMQSAAAAADMrSTJ8f6ggN6ZEj_Sgw-UwI1RD'


# Django storages
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = 'AKIAJ3NVRT46U3FJB7GA'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'kxwheels'
AWS_S3_SECURE_URLS = False


# Celery
#BROKER_HOST = "beta.kxwheels.com"
'''
BROKER_HOST = "192.168.1.112"
BROKER_PORT = 5672
BROKER_USER = "kxwheels"
BROKER_PASSWORD = "1mg01ng1n"
BROKER_VHOST = "kxwheels"
CELERY_RESULT_BACKEND = "amqp"
'''
BROKER_URL = "django://"

# Shipping
SHIPPING_MODULES = ('purolator',)

# Self API Access
API_ACCESS_KEY = "F2A53B2CF070457086347CABC4BDF4E6"

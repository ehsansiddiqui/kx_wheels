from .base import *

ALLOWED_HOSTS = ['.dev.kxwheels.com', '127.0.0.1', '5854fe25.ngrok.io']

MEDIA_URL = '/media/'

SERVER_EMAIL = "mailer@kxwheels.com"
DEFAULT_FROM_EMAIL = "KX Wheels <mailer@kxwheels.com>"
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_USE_TLS = False

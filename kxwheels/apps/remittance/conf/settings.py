from django.conf import settings

SECRET_KEY = getattr(settings, 'SECRET_KEY')
DEBUG = getattr(settings, 'DEBUG')

REMITTANCE_MODULE = getattr(settings, 'REMITTANCE_MODULE', 'offline')

REMITTANCE_SETTINGS = getattr(settings, 'REMITTANCE_SETTINGS', {
    'STORE_CREDIT_NUMBERS' : False,
    'CURRENCY_SYMBOL' : '$' # Use a '_' for force a space
})

PAYMENT_APPROVED_URL = 'shop_payment_approved'
PAYMENT_ERROR_URL = 'shop_payment_error'

CACHE_LIFE = 1800
CACHE_GATEWAY_KEY = 'remittance_gateway'
SESSION_TRANSACTION_KEY = 'remittance_transaction'

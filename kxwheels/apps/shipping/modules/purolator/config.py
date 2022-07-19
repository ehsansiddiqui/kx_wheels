import os
rel = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

## Required Configurations ##
NAME = 'Purolator'

LANG = 'en'

HANDLING_CHARGE_PERCENTAGE = '.10'

LIVE_URL = 'https://webservices.purolator.com/PWS/V1/Estimating/EstimatingService.asmx'
TEST_URL = 'https://webservices.purolator.com/PWS/V1/Estimating/EstimatingService.asmx'
## End Required Configurations ##

KEY = "66e2b8572bab427c864ef6ab319bfd34"
PASSWORD = "D(|>Y|g9"
ACCOUNT = "2006334"

WSDL = "file://{0}".format(rel("./EstimatingService.wsdl"))
URI = "http://purolator.com/pws/datatypes/v1"

SENDER = {
    'Name': 'KX Wheels',
    'StreetNumber': '12A - 3033',
    'StreetName': 'King George Blvd.',
    'City': 'Surrey',
    'Province': 'BC',
    'Country': 'CA',
    'PostalCode': 'V4P1B8',
    'PhoneNumber': {
        'CountryCode': '1',
        'AreaCode': '604',
        'Phone': '5963122'
    },
}

PRODUCTS = [
    'PurolatorGround',
]

SIGNATURE_REQUIRED = True


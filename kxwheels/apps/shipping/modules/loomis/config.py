import os
rel = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

## Required Configurations ##
NAME = 'Loomis'

LANG = 'en'

LIVE_URL = 'https://webservice.loomis-express.com/LShip/services/USSRatingService?wsdl'
TEST_URL = 'https://sandbox.loomis-express.com/axis2/services/USSRatingService?wsdl'
## End Required Configurations ##

USER = "LSHIPRQ7853@NORTHWESTWHEEL.COM"
PASSWORD =  "Nd4Ji04r"
ACCOUNT = "RQ7853"

SENDER = {
    'Name': 'NORTH WEST WHEEL DISTRIBUTORS/KX',
    'StreetNumber': '5570',
    'StreetName': '268TH UNIT 103',
    'City': 'LANGLEY',
    'Province': 'BC',
    'Country': 'CA',
    'PostalCode': 'V4W3X4',
    'PhoneNumber': {
        'CountryCode': '1',
        'AreaCode': '604',
        'Phone': '5963122'
    },
}
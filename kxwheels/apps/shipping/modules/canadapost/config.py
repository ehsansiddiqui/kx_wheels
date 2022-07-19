## Required Configurations ##
NAME = 'Canada Post'

LANG = 'en'

HANDLING_CHARGE = '0.00'

LIVE_URL = 'http://sellonline.canadapost.ca:30000'
TEST_URL = 'http://sellonline.canadapost.ca:30000'
## End Required Configurations ##

CPCID = 'CPC_DEMO_XML'

# Dimentional limits
MAX_WEIGHT = ('30', 'kg')
MAX_LENGTH = ('200', 'cm')
MAX_WIDTH = ('200', 'cm')
MAX_HEIGHT = ('200', 'cm')

PRODUCTS = {
    'available': {
        '1010': 'Domestic - Regular',
        '1020': 'Domestic - Expedited',
        '1030': 'Domestic - Xpresspost',            
        '1040': 'Domestic - Priority Courier',
        '2005': 'US - Small Packets Surface',
        '2015': 'US - Small Packets Air',
        '2020': 'US - Expedited US Business Contract',
        '2025': 'US - Expedited US Commercial',
        '2030': 'US - Xpress USA',
        '2040': 'US - Priority Worldwide USA',
        '2050': 'US - Priority Worldwide PAK USA',
        '3005': 'Int`l - Small Packets Surface',
        '3010': 'Int`l - Surface International',
        '3015': 'Int`l - Small Packets Air',
        '3020': 'Int`l - Air International',
        '3025': 'Int`l - Xpresspost International',
        '3040': 'Int`l - Priority Worldwide INTL',
        '3050': 'Int`l - Priority Worldwide PAK INTL',
    },
    'enabled': ('1010','1020','1030','1040',)
}

CONTAINERS = {
    'available': {
        '00': 'Unknown',
        '01': 'Variable',
        '02': 'Rectangular',
    },
    'enabled': ('00',)
}

# Turn around time of the shipper in hours
TURN_AROUND_TIME = '24'
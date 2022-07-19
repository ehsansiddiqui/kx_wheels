## Required Configurations ##
NAME = 'FedEx'

LANG = 'en'

HANDLING_CHARGE = '0.00'

LIVE_URL = 'https://gateway.fedex.com/GatewayDC'
TEST_URL = 'https://gatewaybeta.fedex.com/GatewayDC'
## End Required Configurations ##

ACCOUNT_NUMBER = '510087046'

METER_NUMBER = '118525255'

DEVELOPER_KEY = '5ampl05i7utVzNf0'

CURRENCY_CODE = 'CAD'

PRODUCTS = {
    'available': {
        'PRIORITYOVERNIGHT': 'Priority Overnight',
        'STANDARDOVERNIGHT': 'Standard Overnight',
        'FIRSTOVERNIGHT': 'First Overnight',
        'FEDEX2DAY': '2 Day',
        'FEDEXEXPRESSSAVER': 'Express Saver',
        'INTERNATIONALPRIORITY': 'International Priority',
        'INTERNATIONALECONOMY': 'International Economy',
        'INTERNATIONALFIRST': 'International First',
        'FEDEX1DAYFREIGHT': '1 Day Freight',
        'FEDEX2DAYFREIGHT': '2 Day Freight',
        'FEDEX3DAYFREIGHT': '3 Day Freight',
        'FEDEXGROUND': 'Ground',
        'GROUNDHOMEDELIVERY': 'Ground Home Delivery',
        'INTERNATIONALPRIORITYFREIGHT': 'International Priority Freight',
        'INTERNATIONALECONOMYFREIGHT': 'International Economy Freight',
        'EUROPEFIRSTINTERNATIONALPRIORITY': 'Europe International Priority',
    },
    'enabled': ('FEDEXGROUND', 'FEDEXEXPRESSSAVER', 'STANDARDOVERNIGHT',
        'INTERNATIONALECONOMY', 'INTERNATIONALPRIORITY',)
}

CARRIER_CODES = {
    'available': {
        'FDXE': 'FedEx Express',
        'FDXG': 'FedEx Ground',
    },
    'enabled': ('FDXG',)
}

CONTAINERS = {
    'available': {
        'FEDEXENVELOPE': 'FEDEXENVELOPE',
        'FEDEXPAK': 'FEDEXPAK',
        'FEDEXBOX': 'FEDEXBOX',
        'FEDEXTUBE': 'FEDEXTUBE',
        'FEDEX10KGBOX': 'FEDEX10KGBOX',
        'FEDEX25KGBOX': 'FEDEX25KGBOX',
        'YOURPACKAGING': 'YOURPACKAGING',
    },
    'enabled': ('YOURPACKAGING',)
}

SINGLE_BOX = True
## Required Configurations ##
NAME = 'Weighted'

LANG = 'en'

HANDLING_CHARGE = '0.00'

LIVE_URL = 'http://www.example.com:80'
TEST_URL = 'http://www.example.com:80'
## End Required Configurations ##

RATES = {
    '1': (1, 25),
    '2': (26, 50),
    '3': (51, 100),
    '4': (101, 200),
    '5': (201, 500),
    '6': (500, 10000),
}

PRODUCTS = {
    'BC': {
        #'rate': ('rate', 'eta')
        '1': ('5.99', '5'),
        '2': ('10.99', '5'),
        '3': ('20.99', '5'),
        '4': ('35.99', '5'),
        '5': ('55.99', '5'),
        '6': ('125.99', '5'),
    },
    'AB': {
        '1': ('7.99', '7'),
        '2': ('13.99', '7'),
        '3': ('24.99', '7'),
        '4': ('42.99', '7'),
        '5': ('78.99', '7'),
        '6': ('135.99', '7'),
    },
    'ON': {
        '1': ('9.99', '8'),
        '2': ('14.99', '8'),
        '3': ('29.99', '8'),
        '4': ('49.99', '8'),
        '5': ('95.99', '8'),
        '6': ('149.99', '8')
    },
    'MI': {
        '1': ('9.99', '8'),
        '2': ('14.99', '8'),
        '3': ('29.99', '8'),
        '4': ('49.99', '8'),
        '5': ('95.99', '8'),
        '6': ('149.99', '8')
    },
}

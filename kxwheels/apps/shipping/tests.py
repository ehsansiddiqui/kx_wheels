import sys
from decimal import Decimal

'''
from shipping import get_modules
from shipping.models import (Seller, Buyer, ParcelItem, Parcel, Product)

seller_info = {
    'name': 'Acme Inc',
    'address': '123 Main St',
    'city': 'Vancouver',
    'province': 'British Columbia',
    'province_code': 'BC',
    'country': 'Canada',
    'country_code': 'CA',
    'postal_code': 'V3W1S9',
    'phone': '6041235555',
    'email': 'support@example.com',
}
buyer_info = seller_info.copy()
buyer_info['postal_code'] = 'V3W9N7'

seller = Seller(**seller_info)
buyer = Buyer(**buyer_info)

item1 = ParcelItem(
    name="Citizen Men's AT0200-05E Eco-Drive Chronograph Canvas Watch",
    qty=1,
    unit_price=Decimal('124.99'),
    weight=(1, 'kg'),
    length=(5, 'cm'),
    width=(8, 'cm'),
    height=(6, 'cm'),
)

item2 = ParcelItem(
    name="Apple iPod nano 8 GB Blue",
    qty=1,
    unit_price=Decimal('139.99'),
    weight=(1.8, 'kg'),
    length=(5, 'cm'),
    width=(8, 'cm'),
    height=(6, 'cm'),    
)

parcel = Parcel()
parcel.add_item(item1)
parcel.add_item(item2)

if __name__=="__main__":

    for module in get_modules():
        shipper = module.Shipper(seller=seller, buyer=buyer, parcel=parcel)
        print shipper.products()
'''


import sys
import urllib2
from suds import WebFault
from suds.client import Client
from suds.sax.element import Element
from suds.transport.https import HttpAuthenticated


KEY = "6d104308e28a4a3e91abffbad5741271"
PASSWORD = "|]yWDU-a"
ACCOUNT = "9999999999"
WSDL = "file:////Users/navi/Projects/kxwheels.com/app/shipping/EstimatingService.wsdl"
LOCATION = "https://devwebservices.purolator.com/PWS/V1/Estimating/EstimatingService.asmx"
URI = "http://purolator.com/pws/datatypes/v1"

http_headers = {
    'trace': True,
    'location': LOCATION,
    'uri': URI,
    'login': KEY,
    'password': PASSWORD,
}


soapheaders = {
    'Version': '1.3',
    'Language': 'en',
    'GroupID': 'xxx',
    'RequestReference': 'Rating Example',
}


sender = {
    'Name': 'Aaron Summer',
    'StreetNumber': '1234',
    'StreetName': 'Main Street',
    'City': 'Surrey',
    'Province': 'BC',
    'Country': 'CA',
    'PostalCode': 'V3W1S9',
    'PhoneNumber': {
        'CountryCode': '1',
        'AreaCode': '604',
        'Phone': '5551234'
    },
}

receiver = {
    'Name': 'Aaron Summer',
    'StreetNumber': '2245',
    'StreetName': 'Douglas Road',
    'City': 'Burnaby',
    'Province': 'BC',
    'Country': 'CA',
    'PostalCode': 'V5C1A1',
    'PhoneNumber': {
        'CountryCode': '1',
        'AreaCode': '604',
        'Phone': '5551234'
    },
}

package = {
    'TotalWeight': {
        'Value': '10',
        'WeightUnit': 'lb',
    },
    'TotalPieces': '1',
    'ServiceID': 'PurolatorExpress',
    'OptionsInformation': {
        'Options': [
            {
                'OptionIDValuePair': {
                    'ID': 'OriginSignatureNotRequired',
                    'Value': 'True',
                }
            }
        ]
    }

}

payment = {
    'PaymentType': 'Sender',
    'BillingAccountNumber': ACCOUNT,
    'RegisteredAccountNumber': ACCOUNT,
}

shipment = {
    'SenderInformation': {
        'Address': sender,
    },
    'ReceiverInformation': {
        'Address': receiver,
    },
    'ShipmentDate': '2012-02-08',
    'PaymentInformation': payment,
    'PackageInformation': package,
    'PickupInformation': {
        'PickupType': 'DropOff',
    },
}

t = HttpAuthenticated(username=KEY, password=PASSWORD)
t.handler = urllib2.HTTPBasicAuthHandler(t.pm)
t.urlopener = urllib2.build_opener(t.handler)

client = Client(WSDL, location=LOCATION, transport=t)

ssnns = ('ns0', URI)
request_context = Element('RequestContext', ns=ssnns)
request_context.insert(Element('RequestReference', ns=ssnns).setText('Rating Example'))
request_context.insert(Element('GroupID', ns=ssnns).setText('xxx'))
request_context.insert(Element('Language', ns=ssnns).setText('en'))
request_context.insert(Element('Version', ns=ssnns).setText('1.3'))


client.set_options(soapheaders=request_context)


try:
    result = client.service.GetFullEstimate(Shipment=shipment, ShowAlternativeServicesIndicator=False)
except WebFault, e:
    print e

print client.last_sent()
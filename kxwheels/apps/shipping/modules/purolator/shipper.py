# TODO: Implement error logging
import urllib2
from datetime import datetime
from decimal import Decimal
from django.conf import settings
from shipping.models import Product
from shipping.modules.base import BaseShipper

from suds import WebFault
from suds.client import Client
from suds.sax.element import Element
from suds.transport.https import HttpAuthenticated

import logging

logger = logging.getLogger("project.project")


class Shipper(BaseShipper):
    """docstring for Shipper"""

    def prepare_context(self):
        pass

    def prepare_request(self):
        shipment = {
            'SenderInformation': {
                'Address': self.config.SENDER,
            },

            'ReceiverInformation': {
                'Address': {
                    'Name': self.buyer.name,
                    'StreetNumber': '',
                    'StreetName': self.buyer.address,
                    'City': self.buyer.city,
                    'Province': self.buyer.province,
                    'Country': self.buyer.country,
                    'PostalCode': self.buyer.postal_code,
                    'PhoneNumber': {
                        'CountryCode': '1',
                        'AreaCode': '',
                        'Phone': self.buyer.phone
                    },
                },
            },

            'ShipmentDate': datetime.now().strftime("%Y-%m-%d"),

            'PaymentInformation': {
                'PaymentType': 'Sender',
                'BillingAccountNumber': self.config.ACCOUNT,
                'RegisteredAccountNumber': self.config.ACCOUNT,
            },

            'PackageInformation': {
                'TotalWeight': {
                    'Value': int(self.parcel.weight[0]),
                    'WeightUnit': self.parcel.weight[1],
                },
                'TotalPieces': sum(item.qty for item in self.parcel.items),
                'ServiceID': self.config.PRODUCTS[0],
                'OptionsInformation': {
                    'Options': [
                        {
                            'OptionIDValuePair': {
                                'ID': 'OriginSignatureNotRequired',
                                'Value': 'True',
                            }
                        },
                    ],
                }
            },

            'PickupInformation': {
                'PickupType': 'DropOff',
            },
        }

        return shipment

    def fetch_response(self):
        if not self.validate():
            return False

        self.prepare_request()

        if settings.DEBUG:
            _shipper_endpoint = self.config.TEST_URL
        else:
            _shipper_endpoint = self.config.LIVE_URL

        if self.response is None:
            t = HttpAuthenticated(username=self.config.KEY, password=self.config.PASSWORD)
            t.handler = urllib2.HTTPBasicAuthHandler(t.pm)
            t.urlopener = urllib2.build_opener(t.handler)

            client = Client(self.config.WSDL, location=_shipper_endpoint, transport=t)

            ssnns = ('ns0', self.config.URI)
            request_context = Element('RequestContext', ns=ssnns)
            request_context.insert(Element('RequestReference', ns=ssnns).setText('Rating Example'))
            request_context.insert(Element('GroupID', ns=ssnns).setText('xxx'))
            request_context.insert(Element('Language', ns=ssnns).setText('en'))
            request_context.insert(Element('Version', ns=ssnns).setText('1.3'))

            client.set_options(soapheaders=request_context)

            shipment = self.prepare_request()

            try:
                result = client.service.GetFullEstimate(Shipment=shipment, ShowAlternativeServicesIndicator=False)
            except WebFault, e:
                result = e

            self.response = result

    def parse_response(self):
        self.fetch_response()
        return self.response

    def products(self):
        """docstring for products"""
        products = []
        response = self.parse_response()

        logger.error(response)

        if isinstance(response, WebFault):
            return tuple()

        if response.ShipmentEstimates and len(response.ShipmentEstimates):
            shipper_products = response.ShipmentEstimates[0]
        else:
            shipper_products = []
        products = []

        for product in shipper_products:
            total_price = Decimal(str(product.TotalPrice))
            rate = total_price + (total_price * Decimal(self.config.HANDLING_CHARGE_PERCENTAGE))

            products.append(Product(
                code=product.ServiceID,
                name="%s - %s" % (self.config.NAME, product.ServiceID),
                rate=rate,
                shipping_date=product.ShipmentDate,
                delivery_date=product.ExpectedDeliveryDate,
            ))

        return tuple(sorted(products, key=lambda item: item.rate))

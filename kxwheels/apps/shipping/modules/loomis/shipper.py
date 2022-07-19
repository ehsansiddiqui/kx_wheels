from datetime import datetime

from django.conf import settings
from zeep import Client
import rollbar

from kxwheels.apps.shipping.models import Product
from kxwheels.apps.shipping.modules.base import BaseShipper
from kxwheels.apps.shipping.exceptions import ServiceUnavailableException, ErroneousResponseException


class Shipper(BaseShipper):
    """docstring for Shipper"""

    def __init__(self, service=None, is_saturday_delivery=False,
                 collect_shipper_number=None, is_residential=False,
                 is_nsr=False, **kwargs):
        self.service = service
        self.is_saturday_delivery = is_saturday_delivery
        self.collect_shipper_number = collect_shipper_number
        self.is_residential = is_residential
        self.is_nsr = is_nsr
        super(Shipper, self).__init__(**kwargs)

    def prepare_context(self):
        pass

    def prepare_request(self):
        request = {
            'user_id': self.config.USER,
            'password': self.config.PASSWORD,
            'shipment': {
                'courier': 'L',
                'delivery_address_line_1': self.buyer.address,
                'delivery_city': self.buyer.city,
                'delivery_country': self.buyer.country,
                'delivery_name': self.buyer.name,
                'delivery_postal_code': self.buyer.postal_code,
                'delivery_province': self.buyer.province,
                'delivery_residential': 'TRUE' if self.is_residential else 'FALSE',

                'dimension_unit': 'I', # Imperial

                'pickup_address_line_1': self.seller.address,
                'pickup_city': self.seller.city,
                'pickup_name': self.seller.name,
                'pickup_postal_code': self.seller.postal_code,
                'pickup_province': self.seller.province,

                'reported_weight_unit': 'L', # Pounds
                'service_type': self.service or 'DD',
                'shipper_num': self.config.ACCOUNT,
                'shipping_date': datetime.now().strftime("%Y%m%d"),

                'user_id': self.config.USER,

                'shipment_info_num': [{
                    'name': 'DECLARED_VALUE',
                    'value': self.parcel.total if self.parcel.total < 2499 else 2499, # Value of order, must be less than 2499
                }],

                'shipment_info_str': [
                    {
                        'name': 'DANGEROUS_GOODS',
                        'value': 'TRUE' if any([pi.is_dangerous for pi in self.parcel.items]) else 'FALSE',
                    },
                    {
                        'name': 'FRAGILE',
                        'value': 'TRUE' if self.parcel.is_fragile else 'FALSE',
                    },
                    {
                        'name': 'NSR',
                        'value': 'TRUE' if self.is_nsr else 'FALSE',
                    },
                    {
                        'name': 'SAT_DELIVERY',
                        'value': 'TRUE' if self.is_saturday_delivery else 'FALSE',
                    }
                ],

                'packages': []
            }
        }

        packages = []
        for parcel_item in self.parcel.items:
            packages.append({
                'package_info_num': [
                    {
                        'name': 'LENGTH',
                        'value': parcel_item.length[0],
                    },
                    {
                        'name': 'WIDTH',
                        'value': parcel_item.width[0],
                    },
                    {
                        'name': 'HEIGHT',
                        'value': parcel_item.height[0],
                    },
                ],
                'package_info_str': [
                    {
                        'name': 'NON_STANDARD',
                        'value': 'FALSE',
                    },
                    {
                        'name': 'SPECIAL_HANDLING',
                        'value': 'FALSE',
                    }
                ],
                'reported_weight': parcel_item.weight[0]
            })

        request['shipment']['packages'] = packages

        if self.collect_shipper_number:
            request['shipment']['collect_shipper_num'] = self.collect_shipper_number

        if self.buyer.address_line_2:
            request['shipment']['delivery_address_line_2'] = self.buyer.address_line_2

        self.request = request
        return request

    def fetch_response(self):
        if not self.validate():
            return False

        if settings.DEBUG:
            _shipper_endpoint = self.config.TEST_URL
        else:
            _shipper_endpoint = self.config.LIVE_URL

        if self.response is None:
            client = Client(_shipper_endpoint)
            shipment = self.prepare_request()

            try:
                result = client.service.getRates(shipment)
            except Exception as e:
                raise e

            self.response = result

    def parse_response(self):
        self.fetch_response()

        # Error handling
        errors = self.response.getRatesResult[0].errors

        if not errors:
            return self.response

        unavailable_error = 'The service is temporary not available.'
        if unavailable_error in errors:
            raise ServiceUnavailableException(unavailable_error)
        else:
            raise ErroneousResponseException(', '.join(errors))

    def products(self):
        products = []

        try:
            response = self.parse_response()
        except Exception as e:
            rollbar.report_exc_info()
            raise e

        if response is None:
            return tuple()

        if response.error is not None:
            return tuple()

        for rate in response.getRatesResult:
            shipment = rate.shipment
            shipping_date = datetime.strptime(shipment.shipping_date, '%Y%m%d')

            delivery_date = None
            if shipment.estimated_delivery_date:
                delivery_date = datetime.strptime(shipment.estimated_delivery_date, '%Y%m%d')

            products.append(Product(
                code=shipment.service_type,
                name="%s Ground" % self.config.NAME,
                rate=self._get_total_charge(),
                shipping_date=shipping_date.strftime('%Y-%m-%d'),
                delivery_date=delivery_date.strftime('%Y-%m-%d') if delivery_date else None,
            ))

        return products

    def _get_base_charge(self):
        shipment_info = self.response.getRatesResult[0].shipment.shipment_info_num
        charge = [info['value'] for info in shipment_info
                       if info['name'] == "BASE_CHARGE"]
        if charge:
            return charge[0]
        return "0"

    def _get_freight_charge(self):
        shipment = self.response.getRatesResult[0].shipment
        return shipment.freight_charge

    def _get_fuel_surcharge(self):
        shipment = self.response.getRatesResult[0].shipment
        return shipment.fuel_surcharge

    def _get_add_ser_charge(self):
        shipment_info = self.response.getRatesResult[0].shipment.shipment_info_num
        charge = [info['value'] for info in shipment_info
                       if info['name'] == "ADD_SER_CHARGE"]
        if charge:
            return charge[0]
        return "0"

    def _get_tax_charge_1(self):
        shipment = self.response.getRatesResult[0].shipment
        return shipment.tax_charge_1

    def _get_tax_charge_2(self):
        shipment = self.response.getRatesResult[0].shipment
        return shipment.tax_charge_2

    def _get_total_charge(self):
        shipment_info = self.response.getRatesResult[0].shipment.shipment_info_num
        charge = [info['value'] for info in shipment_info
                  if info['name'] == "TOTAL_CHARGE"]
        if charge:
            return charge[0]
        return "0"

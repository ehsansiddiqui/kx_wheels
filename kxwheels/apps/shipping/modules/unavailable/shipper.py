from datetime import date, timedelta
from kxwheels.apps.shipping.models import Product
from kxwheels.apps.shipping.modules.base import BaseShipper


class Shipper(BaseShipper):
    """docstring for Shipper"""

    def prepare_context(self):
        return {}

    def fetch_response(self):
        pass

    def products(self):
        """docstring for products"""
        _date_format = "%Y-%m-%d"

        temp_product = Product(
            code='temp',
            name='Service Unavailable (Cost TBD)',
            rate=0,
            shipping_date=date.today().strftime(_date_format),
            delivery_date=(date.today() + timedelta(days=7)).strftime(_date_format),
        )
        return ([temp_product, ])

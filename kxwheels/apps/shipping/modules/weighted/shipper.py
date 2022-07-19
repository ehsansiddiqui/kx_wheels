from datetime import date, timedelta
from kxwheels.apps.shipping.models import Product
from kxwheels.apps.shipping.modules.base import BaseShipper
from kxwheels.apps.shipping.templatetags.shipping_tags import unit

class Shipper(BaseShipper):
    """docstring for Shipper"""
    def prepare_context(self):
        context = {}
        return context
        
    def fetch_response(self):
        pass
    
    def products(self):
        """docstring for products"""
        products = []
        _province = self.buyer.province.upper()
        _weight = unit(self.parcel.weight, 'kg')
        _rate = None
        
        for rate, weight in self.config.RATES.iteritems():
            if _weight >= weight[0] and _weight < weight[1]:
                _rate = rate
                break
        
        _date_format = "%Y-%m-%d"
        
        # Fix this
        try:
            rate = self.config.PRODUCTS[_province][_rate][0]
            days = int(self.config.PRODUCTS[_province][_rate][1])
            product = Product(
                code='stock',
                name='Standard',
                rate=rate,
                shipping_date=date.today().strftime(_date_format),
                delivery_date=(date.today()+timedelta(days=days)).strftime(_date_format),
            )
        except Exception as e:
            pass
        else:
            products.append(product)

        temp_product = Product(
            code='temp',
            name='FREIGHT TO BE DETERMINED AFTER ORDER',
            rate=0,
            shipping_date=date.today().strftime(_date_format),
            delivery_date=(date.today() + timedelta(days=7)).strftime(_date_format),
        )
        return ([temp_product, ])

        return tuple(sorted(products, key=lambda item: item.rate))
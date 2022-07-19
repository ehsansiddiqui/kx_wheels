from datetime import (datetime, date, timedelta)
from shipping.models import Product
from shipping.modules.base import BaseShipper

class Shipper(BaseShipper):
    """docstring for Shipper"""
    def prepare_context(self):
        context = {
            'ship_date': (date.today()+timedelta(days=1)),
        }
        return context
            
    def products(self):
        """docstring for products"""
        products = []
        response = self.parse_response()
        elements = response.findAll('entry')
        
        for e in elements:
            _date_format = "%Y-%m-%d"
            shipping_date = self.prepare_context()['ship_date']
            delivery_date = (shipping_date + timedelta(days=\
                int(e.find('timeintransit').text)))
        
            products.append(Product(
                code=e.find('service').text,
                name="%s - %s" % (self.config.NAME, e.find('service').text),
                rate=e.find('netcharge').text,
                shipping_date=shipping_date.strftime(_date_format),
                delivery_date=delivery_date.strftime(_date_format),
            ))

        return tuple(sorted(products, key=lambda item: item.rate))

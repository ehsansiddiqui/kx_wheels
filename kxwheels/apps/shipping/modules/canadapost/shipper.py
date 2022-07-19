from shipping.models import Product
from shipping.modules.base import BaseShipper

class Shipper(BaseShipper):
    """docstring for Shipper"""
    def prepare_context(self):
        context = {}
        return context

    def products(self):
        """docstring for products"""
        products = []
        response = self.parse_response()
        elements = response.findAll('product')
            
        for e in elements:
            product = Product(
                code=e['id'],
                name="%s - %s" % (self.config.NAME, e.find('name').text),
                rate=e.find('rate').text,
            )

            try:
                shipping_date=e.find('shippingdate').text,
            except ValueError:
                shipping_date=None

            try:
                delivery_date=e.find('deliverydate').text,
            except ValueError:
                delivery_date=None
            
            products.append(product)
        return tuple(sorted(products, key=lambda item: item.rate))
        
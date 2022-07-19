from datetime import date, datetime
from decimal import Decimal

import copy


class Entity(object):
    def __init__(self, name=None, address=None, address_line_2=None,
                 city=None, province=None, postal_code=None,
                 country=None, phone=None, email=None):
        self.name = name
        self.address = address
        self.address_line_2 = address_line_2
        self.city = city
        self.province = province
        self.postal_code = postal_code
        self.country = country
        self.phone = phone
        self.email = email
    
    def __repr__(self):
        return u"<Entity: %s>" % self.name
    
    def __str__(self):
        return self.__repr__()

    def __unicode__(self):
        return self.__repr__()
                
class Seller(Entity):
    def __init__(self, *args, **kwargs):
        super(Seller, self).__init__(*args, **kwargs)
    
    def __repr__(self):
        return u"<Seller: %s>" % self.name
    
class Buyer(Entity):
    def __init__(self, *args, **kwargs):
        super(Buyer, self).__init__(*args, **kwargs)

    def __repr__(self):
        return u"<Buyer: %s>" % self.name

class ParcelItem(object):
    def __init__(self, name=None, qty=None, unit_price=None, weight=None,
                 length=None, width=None, height=None, is_dangerous=False):
        self.name = name
        self.qty = int(qty)
        self.unit_price = Decimal(unit_price)
        self.is_dangerous = is_dangerous

        self.weight = (0, 'kg')
        if weight is not None:
            self.weight = (weight[0], weight[1])

        self.length = (0, 'cm')
        if length is not None:
            self.length = (length[0], length[1])

        self.width = (0, 'cm')
        if width is not None:
            self.width = (width[0], width[1])

        self.height = (0, 'cm')
        if height is not None:
            self.height = (height[0], height[1])

    @property
    def sub_total(self):
        return (self.unit_price * self.qty)
    
    def __repr__(self):
        return u"<ParcelItem: %s>" % self.name

    def __str__(self):
        return self.__repr__()

    def __unicode__(self):
        return self.__repr__()

class Parcel(object):
    def __init__(self, items=None, is_fragile=False):
        if items is None:
            items = []

        self.items = []
        for item in items:
            for index in range(item.qty):
                self.items.append(copy.deepcopy(item))
        self.is_fragile = is_fragile
        
    def add_item(self, item):
        assert isinstance(item, ParcelItem)
        self.items.append(item)

    @property
    def total(self):
        _total = sum([item.sub_total for item in self.items])
        return _total
        
    @property
    def weight(self):
        try:
            _weight = (sum([item.weight[0]*item.qty for item in self.items]),
                       self.items[0].weight[1])
        except:
            _weight = 0
        return _weight

    def __repr__(self):
        return u"<Parcel: %s item(s) totalling $%s>" % \
            (len(self.items), self.total)

    def __str__(self):
        return self.__repr__()

    def __unicode__(self):
        return self.__repr__()
        
class Product(object):
    """Not a store product but a product/service provided by the shipping company"""
    def __init__(self, code=None, name=None, rate=None, shipping_date=None, 
        delivery_date=None, extra_info=None):
        _date_format = "%Y-%m-%d"
        self.code = code
        self.name = name
        self.rate = Decimal(rate)
        self.shipping_date = shipping_date
        self.delivery_date = delivery_date
        self.extra_info = extra_info
        
        if self.shipping_date is not None:
            self.shipping_date = datetime.strptime(shipping_date, _date_format)
        if self.delivery_date is not None:
            self.delivery_date = datetime.strptime(delivery_date, _date_format)
        
        
    @property
    def days(self):
        if None in (self.shipping_date, self.delivery_date):
            return False

        assert isinstance(self.shipping_date, date)
        assert isinstance(self.delivery_date, date)

        delta = self.delivery_date - self.shipping_date
        result = delta.days
        return result
        
    @property
    def delivery_day(self):
        assert isinstance(self.delivery_date, date)
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
            'Saturday', 'Sunday' ]
        return days_of_week[date.weekday(self.delivery_date)]
    
    def __repr__(self):
        if self.delivery_date:
            return u"<Product: %s (%s) - %s>" % (self.name, 
                self.delivery_date.strftime('%Y-%m-%d'), self.rate)
        else:
            return u"<Product: %s - %s>" % (self.name, self.rate)        

    def __str__(self):
        return self.__repr__()

    def __unicode__(self):
        return self.__repr__()
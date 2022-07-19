import urllib2
from django.conf import settings
from importlib import import_module
from django.template import loader, Context
from BeautifulSoup import BeautifulStoneSoup
from kxwheels.apps.shipping.models import Seller, Buyer, Parcel


class BaseShipper(object):
    """docstring for BaseShipper"""
    def __init__(self, name=None, seller=None, buyer=None, parcel=None):
        self.name = self.__module__.split('.')[-2]
        self.seller = seller
        self.buyer = buyer
        self.parcel = parcel
        self.config = import_module('.config', 'kxwheels.apps.shipping.modules.%s' % self.name)
        
        self.request = None
        self.response = None

    def __repr__(self):
        return u"<Shipper: %s>" % self.name

    def __str__(self):
        """docstring for __str__"""
        return self.__repr__()

    def __unicode__(self):
        """docstring for __unicode__"""
        return self.__repr__()

    def validate(self):
        """docstring for validate"""
        assert isinstance(self.seller, Seller)
        assert isinstance(self.buyer, Buyer)
        assert isinstance(self.parcel, Parcel)
        
        assert self.config.NAME != ''
        assert self.config.LANG != ''
        #assert self.config.HANDLING_CHARGE != ''
        assert self.config.LIVE_URL != ''
        assert self.config.TEST_URL != ''
        
        if None in [self.seller, self.buyer, self.parcel]:
            return False
        return True
        
    def prepate_context(self):
        """docstring for prepate_context"""
        return dict()
        
    def prepare_request(self):
        """This function must render the request template"""
        context = {
            'config': self.config,
            'parcel': self.parcel,
            'buyer': self.buyer,
            'seller': self.seller,
        }
        
        context['extra'] = self.prepare_context()
        template = loader.get_template('shipping/%s/request.xml' % self.name)
        self.request = template.render(Context(context))
        return True
        
    def fetch_response(self):
        """docstring for perform_request"""
        if not self.validate():
            return False
        
        self.prepare_request()
        
        if settings.DEBUG:
            _shipper_endpoint = self.config.TEST_URL
        else:
            _shipper_endpoint = self.config.LIVE_URL

        if self.response is None:
            conn = urllib2.Request(url=_shipper_endpoint, data=self.request)
            fsock = urllib2.urlopen(conn)
            response = fsock.read()
            fsock.close()
            self.response = response
        
    def parse_response(self):
        self.fetch_response()
        
        parsed_data = BeautifulStoneSoup(self.response)
        return parsed_data
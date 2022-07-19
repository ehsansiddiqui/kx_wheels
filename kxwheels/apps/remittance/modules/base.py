import json
import random
import urllib
import urllib2
import uuid
from decimal import Decimal

from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect

from kxwheels.apps.remittance import get_module
from kxwheels.apps.remittance.conf import settings
from kxwheels.apps.remittance.exceptions import (NonPositiveBalanceError,
                                                 MissingConfigurationError,
                                                 InvalidGatewayError, GatewayError)
from kxwheels.apps.remittance.models import (Seller, Buyer, Purchase, PurchaseItem)


class BaseGateway(object):
    def __init__(self, *args, **kwargs):
        super(BaseGateway, self).__init__()
        self.id = uuid.uuid4().hex
        self.name = self.__module__.split('.')[-2]
        self.config = getattr(get_module(), 'settings')
        self.site = Site.objects.get_current()
        self.request = None
        self.response = None

    def __str__(self):
        return self.__repr__()

    def __unicode__(self):
        return self.__repr__()

    # Get configuration value
    def get_config(self, key):
        result = ""
        try:
            result = self.config[key]
        except KeyError as e:
            raise MissingConfigurationError(e)
        return result
        
    # To validate fields before any operation
    def validate(self):
        pass
        
    # To initialize the payment procedure
    def initialize(self):
        if self.validate():
            return HttpResponseRedirect(reverse('remittance_payment'))
        
        # Control must not reach here
        return 
    
    # To prepare request data that will be submitted to payment processor
    def prep_request(self):
        pass
    
    # To send the actual request and fetch the response
    def send_request(self):
        pass

    # To parse the response sent by the payment processor
    def parse_response(self):
        pass

    # To call the parse_response function and save the data
    def get_response(self):
        pass


class BaseEmption(BaseGateway):
    def __init__(self, seller, buyer, purchase, purchase_items):
        super(BaseEmption, self).__init__()
        self.form = None
        self.seller = seller
        self.buyer = buyer
        self.purchase = purchase
        self.purchase_items = purchase_items


        
    def __repr__(self):
        return u"<Emption: %s>" % self.name

    # Helper function
    def validate(self):
        if not isinstance(self.seller, Seller):
            raise InvalidGatewayError("Invalid seller information.")

        if not isinstance(self.buyer, Buyer):
            raise InvalidGatewayError("Invalid buyer information.")

        if not isinstance(self.purchase, Purchase):
            raise InvalidGatewayError("Invalid purchase information.")

        if not isinstance(self.purchase_items, list):
            raise InvalidGatewayError("Invalid purchase items information. It \
                                        should be a list of instances of \
                                        PurchaseItem.")

        if not len(self.purchase_items) > 0:
            raise InvalidGatewayError("There should at least be one purchase \
                                        items.")

        for item in self.purchase_items:
            if not isinstance(item, PurchaseItem):
                raise InvalidGatewayError("Invalid purchase item information.")

        name, lang, live_url, test_url = self.get_config('NAME'), \
                                         self.get_config('LANG'), \
                                         self.get_config('LIVE_URL'), \
                                         self.get_config('TEST_URL')

        if "" in [name, lang, live_url, test_url]:
            raise InvalidGatewayError("Gateway configuration is missing \
                                        required configuration settings")

        return True

    def send_request(self):
        # Initiate request
        self.request = self.prep_request()

         # Balance must be greater than 0.00
        if self.purchase.get_balance() <= Decimal('0.00'):
             self.response = "Balance must be greater than zero"
             raise NonPositiveBalanceError(self.response)

        if settings.DEBUG:
            endpoint = self.get_config('TEST_URL')
        else:
            endpoint = self.get_config('LIVE_URL')

        headers = {
            'User-Agent': 'Django-Remittance/0.1',
            'Connection': 'keep-alive'
        }

        if self.request is not None:
            request_data = urllib.urlencode(self.request)
            conn = urllib2.Request(url=endpoint,
                                   data=request_data,
                                   headers=headers)

            try:
                fsock = urllib2.urlopen(conn)
            except:
                raise GatewayError(instance=self)
            else:
                response = fsock.read()
                fsock.close()

            self.response = response
        return self.response

    def get_response(self, form):
        self.form = form

        # Save the transaction response
        response = self.parse_response()

        transaction = response.save()
        return transaction

    def auth_trans(self, key):
        pass
        
class BasePreAuth(BaseEmption):
    def __init__(self, seller=None, buyer=None, purchase=None):
        super(BasePreAuth, self).__init__()
        self.name = self.__module__.split('.')[-2]
        self.seller = seller
        self.buyer = buyer
        self.purchase = purchase
        self.config = getattr(get_module(), 'settings')
        self.site = Site.objects.get_current()
        self.request = None
        self.response = None
        
    def __repr__(self):
        return u"<Pre-Authorization: %s>" % self.name

# TODO: Configure capturing for gateways that support it
class BaseCapture(BaseGateway):
    def __init__(self, order_id=None, trans_id=None, amount=None):
        super(BaseCapture, self).__init__()
        self.name = self.__module__.split('.')[-2]
        self.order_id = order_id
        self.trans_id = trans_id
        self.amount = amount
        self.config = getattr(get_module(), 'settings')
        self.site = Site.objects.get_current()
        self.request = None
        self.response = None
        
    def __repr__(self):
        return u"<Capture: %s>" % self.name

    def process_request(self):
        response = self.parse_response()
        
        if response:
            response.save()
            # Capture approved
            return HttpResponse('Capture completed successfully.')
        else:
            # Capture error or declined
            return HttpResponse('Error occured while capturing.')

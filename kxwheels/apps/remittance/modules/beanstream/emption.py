import urllib
import hashlib
import urlparse
from datetime import datetime
from django.core.urlresolvers import reverse
from kxwheels.apps.remittance.modules.base import BaseEmption
from kxwheels.apps.remittance.models import Response, TRANSACTION_TYPES

class Emption(BaseEmption):

    def prep_request(self):
        if self.purchase.currency == 'CAD':
            mid = self.get_config('CAD_MERCHANT_ID')
        else:
            mid = self.get_config('USD_MERCHANT_ID')
            
        request_dict = {
            'merchant_id':mid,
            'requestType':'BACKEND',
            'trnType':'P',
            'trnOrderNumber':self.purchase.pk,
            'trnAmount':self.purchase.get_balance(),
            
            'trnCardOwner':self.form.cleaned_data['name'],
            'trnCardNumber':self.form.cleaned_data['number'],
            'trnExpMonth':self.form.cleaned_data['exp_month'],
            'trnExpYear':self.form.cleaned_data['exp_year'],
            'trnCardCvd':self.form.cleaned_data['cvd'],
            
            'ordItemPrice': self.purchase.subtotal,
            'ordTax1Price': '',
            'ordTax2Price': '',
            'ordShippingPrice': self.purchase.shipping,
            
            'ordName':self.buyer.billing_full_name,
            'ordAddress1':self.buyer.billing_address_1,
            'ordAddress2':self.buyer.billing_address_2,
            'ordCity':self.buyer.billing_city,
            'ordProvince':self.buyer.billing_province,
            'ordCountry':self.buyer.billing_country,
            'ordPostalCode':self.buyer.billing_postal_code,
            'ordPhoneNumber':self.buyer.billing_phone,
            'ordEmailAddress':self.buyer.email,
            
            'shipName': self.buyer.shipping_full_name,
            'shipAddress1':self.buyer.shipping_address_1,
            'shipAddress2':self.buyer.shipping_address_2,
            'shipCity':self.buyer.shipping_city,
            'shipProvince':self.buyer.shipping_province,
            'shipCountry':self.buyer.shipping_country,
            'shipPostalCode':self.buyer.shipping_postal_code,
            'shipPhoneNumber': self.buyer.shipping_phone,
            'shipEmailAddress': self.buyer.email,
            'shippingMethod': '',
            'deliveryEstimate': '', # In days
            'shippingRequired': '1',
            'notes': self.form.cleaned_data['notes']
        }
        
        for index, item in enumerate(self.purchase.items.all()):
            request_dict["prod_id_%s" % int(index+1)] = item.sku
            request_dict["prod_name_%s" % int(index+1)] = item.name
            request_dict["prod_quantity_%s" % int(index+1)] = item.qty
            request_dict["prod_cost_%s" % int(index+1)] = item.unit_price

        # Convert request_dict dictionary to list of tuples
        request_list = [(k, v) for k, v in request_dict.iteritems()]
        # Create querystring from request dict and append hash key
        request_plain = urllib.urlencode(request_dict) + self.config['HASH_KEY']
        # Create hash of the above
        request_hash = hashlib.sha1(request_plain).hexdigest()
        # Append hash to the request dict
        request_list.append(('hashValue', request_hash))
        
        return request_list
        
    def parse_response(self):
        raw_response = self.send_request()
        _response = urlparse.parse_qs(raw_response)

        if not _response:
            return False
        
        if 'authCode' in _response.keys():
            authCode = _response.get('authCode')[0]
        else:
            authCode = ''
        
        response = Response(
            purchase=_response.get('trnOrderNumber')[0],
            trans_id=_response.get('trnId')[0],
            trans_type=TRANSACTION_TYPES[_response.get('trnType')[0]],
            method=_response.get('paymentMethod')[0],
            gateway=self.get_config('NAME'),
            amount=_response.get('trnAmount')[0],
            trans_datetime=datetime.strptime(_response.get('trnDate')[0], '%m/%d/%Y %I:%M:%S %p'),
            auth_code=authCode,
            iso_code='NA',
            response_code=_response.get('messageId')[0],
            reason_code='NA',
            message=_response.get('messageText')[0],
            raw=raw_response,
            paypal_email=_request.get('notes')
        )
        if _response.get('trnApproved')[0] == '1':
            response.is_success = True
        else:
            response.is_success = False
        
        return response
        

#TODO: Convert from direct post to XML based requests
import urlparse
from datetime import datetime
from django.core.urlresolvers import reverse
from kxwheels.apps.remittance.modules.base import BaseEmption
from kxwheels.apps.remittance.models import Response

class Emption(BaseEmption):

    def prep_request(self):
        '''
        header = "<?xml version=\"1.0\"?>"\
            + "<request>"\
            + "<store_id>" + self.config['PS_STORE_ID'] + "</store_id>"\
            + "<api_token>" + self.api_token + "</api_token>"
        '''
        
        request_dict = {
            'ps_store_id': self.config['PS_STORE_ID'],
            'hpp_key': self.config['HPP_KEY'],
            'charge_total': self.purchase.get_balance(),
            'cc_num': self.form.cleaned_data['number'],
            'expMonth': self.form.cleaned_data['exp_month'], 
            'expYear': self.form.cleaned_data['exp_year'],
            'cvd_value': self.form.cleaned_data['cvd'],
            'cvd_indicator': '1',
            #'avs_street_number':,
            #'avs_street_name':,
            #'avs_zipcode':self.buyer.postal_code,
            'cust_id': self.buyer.email,
            'order_id': self.purchase.pk,
            'lang': 'en-ca',
            'gst': '',
            'pst': '',
            'hst': self.purchase.tax,
            'shipping_cost': self.purchase.shipping,
            'note': self.purchase.note,
            
            # Billing details
            'bill_first_name': self.buyer.billing_first_name,
            'bill_last_name': self.buyer.billing_last_name,
            'bill_company_name': '',
            'bill_address_one': self.buyer.billing_address_1,
            'bill_city': self.buyer.billing_city,
            'bill_state_or_province': self.buyer.billing_province,
            'bill_postal_code': self.buyer.billing_postal_code,
            'bill_country': self.buyer.billing_country,
            'bill_phone': self.buyer.billing_phone,
            'bill_fax': '',
            
            # Shipping details
            'ship_first_name': self.buyer.shipping_first_name,
            'ship_last_name': self.buyer.shipping_last_name,
            'ship_company_name': '',
            'ship_address_one': self.buyer.shipping_address_1,
            'ship_city': self.buyer.shipping_city,
            'ship_state_or_province': self.buyer.shipping_province,
            'ship_postal_code': self.buyer.shipping_postal_code,
            'ship_country': self.buyer.shipping_country,
            'ship_phone': self.buyer.shipping_phone,
            'ship_fax': '',
            'notes': self.form.cleaned_data['notes']
        }
        
        for index, item in enumerate(self.purchase.items.all()):
            request_dict["id%s" % int(index+1)] = item.sku
            request_dict["description%s" % int(index+1)] = item.name
            request_dict["quantity%s" % int(index+1)] = item.qty
            request_dict["price%s" % int(index+1)] = item.unit_price
            request_dict["subtotal%s" % int(index+1)] = item.ext_price
            
        return request_dict

    def parse_response(self):
        raw_response = self.send_request()
        _reponse_list = raw_response.split("<br>")
        _response = {}
        for _field in _reponse_list:
            key, value = _field.split(' = ')
            _response[key.strip()] = value.strip()

        if 'result' not in _response.keys():
            return False
        
        if _response.get('result') == '1':
            _trans_datetime = "%s %s" % (_response.get('date_stamp'), _response.get('time_stamp'))
            _trans_datetime = datetime.strptime(_trans_datetime, '%Y-%m-%d %H:%M:%S')
        else:
            _trans_datetime = datetime.now()

        response = Response(
            purchase=_response.get('response_order_id'),
            trans_id=_response.get('bank_transaction_id'),
            trans_type=_response.get('trans_name'),
            method=_response.get('card'),
            gateway=self.config['NAME'],
            amount=_response.get('charge_total'),
            trans_datetime=_trans_datetime,
            auth_code=_response.get('bank_approval_code'),
            iso_code=_response.get('iso_code'),
            response_code=_response.get('response_code'),
            reason_code='NA',
            message=_response.get('message'),
            raw=raw_response,
            paypal_email=_request.get('notes')
        )
        if _response.get('result') == '1':
            response.is_success = True
        else:
            response.is_success = False

        return response

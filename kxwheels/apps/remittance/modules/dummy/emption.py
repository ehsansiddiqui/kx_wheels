import urllib
import hashlib
import urlparse
from random import randint
from decimal import Decimal
from time import gmtime, strftime
from datetime import datetime
from django.core.urlresolvers import reverse
from kxwheels.apps.remittance.modules.base import BaseEmption
from kxwheels.apps.remittance.models import Response

class Emption(BaseEmption):

    def prep_request(self):
        request_dict = dict(modname=self.get_config('NAME'),
                            order_number=self.purchase.order,
                            amount=self.purchase.get_balance(),
                            name=self.form.cleaned_data['name'],
                            type=self.form.cleaned_data['type'],
                            number=self.form.cleaned_data['number'],
                            exp_month=self.form.cleaned_data['exp_month'],
                            exp_year=self.form.cleaned_data['exp_year'],
                            cvd=self.form.cleaned_data['cvd'],
                            notes=self.form.cleaned_data['notes'])
        return request_dict
        
    def parse_response(self):
        _request = self.prep_request()
        
        _response = dict(order_number=_request.get('order_number'),
                         transaction_id=randint(1111111111, 9999999999),
                         transaction_type='P', method='Credit Card',
                         amount=Decimal(_request.get('amount')),
                         datetime=strftime("%m/%d/%Y %I:%M:%S %p", gmtime()),
                         auth_code='999', iso_code='1', message_id='101',
                         message='Not Approved', is_approved='0')
        
        response = Response(
            purchase=_response.get('order_number'),
            trans_id=_response.get('transaction_id'),
            trans_type=_response.get('transaction_type'),
            method=_response.get('method'),
            gateway=self.name,
            amount=_response.get('amount'),
            trans_datetime=datetime.strptime(_response.get('datetime'), '%m/%d/%Y %I:%M:%S %p'),
            auth_code=_response.get('auth_code'),
            iso_code=_response.get('iso_code'),
            response_code=_response.get('message_id'),
            reason_code='NA',
            message=_response.get('message'),
            raw=_response,
            paypal_email=_request.get('notes')
        )

        if _response.get('is_approved') == '1':
            response.is_success = True
        else:
            response.is_success = False
        
        return response


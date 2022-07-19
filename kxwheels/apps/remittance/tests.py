import random
from decimal import Decimal
from datetime import datetime
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from kxwheels.apps.remittance import Emption
from kxwheels.apps.remittance.models import *
from kxwheels.apps.remittance.conf import settings
    
class PurchaseTestCase(TestCase):
    # Here's what this application expects:
    # Instances of Buyer, Seller, Purchase
    # and a list of instances of PurchaseItem

    def setUp(self):
        self.client = Client()

        self.seller = Seller(
            company_name='Your company name',
            address_1='123 Main St.',
            address_2='',
            city='Vancouver',
            province='BC',
            postal_code='V3W 2Z6',
            country='CA',
            phone='604-555-1234',
            email='order@example.com',
        )

        self.buyer = Buyer(
            email='joe@example.com',
            billing_first_name='Joe',
            billing_last_name='Johnson',
            billing_address_1='6274 Green Ave.',
            billing_address_2='',
            billing_city='Burnaby',
            billing_province='BC',
            billing_postal_code='V3W 0T1',
            billing_country='CA',
            billing_phone='604-123-5555',
            # Leave shipping address if it is same as billing
        )

        self.purchase = Purchase(
            order='ORD%d' % random.randint(1111,9999),
            subtotal='13.96',
            tax='1.66',
            shipping='5.99',
            discount='-2.99',
            total='18.62',
            note='',
            currency='CAD',
        )

        self.purchase_items = []
        self.purchase_items.append(PurchaseItem(
            sku='SKU%d' % random.randint(1111,9999),
            name='No-name widget',
            desc='',
            qty='3',
            unit_price='2.99',
            discount='-0.00',
            ext_price='8.97',
            tax='1.08',
        ))

        self.purchase_items.append(PurchaseItem(
            sku='SKU%d' % random.randint(1111,9999),
            name='Another no-name widget',
            desc='',
            qty='1',
            unit_price='4.99',
            discount='-0.00',
            ext_price='4.99',
            tax='0.59',
        ))
        
    def tearDown(self):
        self.seller.save()
        self.buyer.save()
        self.purchase.save()
        for item in self.purchase_items:
            item.purchase = self.purchase
            item.save()
        self.test_buyer_address()
        self.test_emption()

    def test_buyer_address(self):
        ADDRESS_FIELDS = [
            'first_name',
            'last_name',
            'company_name',
            'address_1',
            'address_2',
            'city',
            'province',
            'postal_code',
            'country',
            'email',
            'phone',
            'fax',
        ]
        
        self.assertNotEqual(self.buyer.pk, None)
        
        if self.buyer.is_shipping_same_billing:
            for field in ADDRESS_FIELDS:
                self.assertEqual(
                    getattr(self.buyer, 'shipping_%s' % field),
                    getattr(self.buyer, 'billing_%s' % field),
                )
        return
        
    def test_emption(self):
        client = self.client
        seller = self.seller
        buyer = self.buyer
        purchase = self.purchase
        purchase_items = self.purchase_items

        result = Emption(seller, buyer, purchase, purchase_items)
        t = result
        
        assert isinstance(t, Transaction)
        assert isinstance(t.purchase, Purchase)
        self.assertEqual(t.trans_type, 'purchase')
        self.assertEqual(t.amount, Decimal('18.62'))
        
        # Module specific results. Change accordingly
        self.assertEqual(t.method, 'Credit Card')
        self.assertEqual(t.gateway, 'Dummy')
        self.assertEqual(t.auth_code, '999')
        self.assertEqual(t.iso_code, '1')
        self.assertEqual(t.response_code, '101')
        self.assertEqual(t.reason_code, 'NA')
        self.assertEqual(t.message, 'Approved')
        
        self.assertEqual(t.is_success, True)

from decimal import Decimal

import datetime
from prettyprint import pp
from django.test import TestCase
from kxwheels.apps.shipping.models import Seller, Buyer, Parcel, ParcelItem
from .shipper import Shipper

seller = Seller(name='KX Wheels',
                address='12A - 3033 King George Blvd.',
                city='Surrey',
                province='BC',
                postal_code='V4P1B8',
                country='CA',
                phone='6045963122',
                email='info@kxwheels.com', )


# class TestShippingMethod(TestCase):
#     def setUp(self):
#         self.seller = seller
#
#         self.buyer = Buyer(name='Rickety Cricket',
#                            address='12788 76A Ave',
#                            city='Surrey',
#                            province='BC',
#                            postal_code='V3W1S9',
#                            country='CA',
#                            phone='6045551323',
#                            email='info@shiftonline.com', )
#
#         parcel_item = ParcelItem(name="21 Inch Wheel Specials - TSW - Nurburgring - Matte Gunmetal",
#                                  qty=4,
#                                  unit_price="400.00",
#                                  weight=(11*4, 'kg'))
#
#         self.parcel = Parcel(items=[parcel_item,])
#
#         self.response = {
#             'error': None,
#             'getRatesResult': [
#                 {
#                     'errors': [],
#                     'messages': [],
#                     'shipment': {
#                         'billed_weight': Decimal('44.0'),
#                         'billed_weight_unit': 'L',
#                         'collect_shipper_num': None,
#                         'consolidation_type': None,
#                         'courier': 'L',
#                         'delivery_address_id': None,
#                         'delivery_address_line_1': '12788 76A AVE',
#                         'delivery_address_line_2': None,
#                         'delivery_address_line_3': None,
#                         'delivery_city': 'SURREY',
#                         'delivery_country': 'CA',
#                         'delivery_email': None,
#                         'delivery_extension': None,
#                         'delivery_name': 'RICKETY CRICKET',
#                         'delivery_phone': None,
#                         'delivery_postal_code': 'V3W1S9',
#                         'delivery_province': 'BC',
#                         'delivery_residential': True,
#                         'dimension_unit': 'I',
#                         'estimated_delivery_date': None,
#                         'freight_charge': Decimal('0.00'),
#                         'fuel_surcharge': Decimal('2.62'),
#                         'id': -1L,
#                         'inserted_on': datetime.datetime(2017, 4, 16, 15, 41, 38, 613000),
#                         'manifest_num': None,
#                         'packages': [
#                             {
#                                 'billed_weight': Decimal('44.0'),
#                                 'dim_weight': Decimal('0.0'),
#                                 'dim_weight_flag': False,
#                                 'id': -1L,
#                                 'inserted_on': datetime.datetime(2017, 4, 16, 15, 41, 38, 613000),
#                                 'min_weight_flag': False,
#                                 'package_info_num': [
#                                     {
#                                         'id': -1L,
#                                         'inserted_on': datetime.datetime(2017, 4, 16, 15, 41, 38, 613000),
#                                         'name': 'LENGTH',
#                                         'updated_on': datetime.datetime(2017, 4, 16, 15, 41, 38, 613000),
#                                         'value': Decimal('0.00')
#                                     },
#                                     {
#                                         'id': -1L,
#                                         'inserted_on': datetime.datetime(2017, 4, 16, 15, 41, 38, 613000),
#                                         'name': 'WIDTH',
#                                         'updated_on': datetime.datetime(2017, 4, 16, 15, 41, 38, 613000),
#                                         'value': Decimal('0.00')
#                                     },
#                                     {
#                                         'id': -1L,
#                                         'inserted_on': datetime.datetime(2017, 4, 16, 15, 41, 38, 613000),
#                                         'name': 'HEIGHT',
#                                         'updated_on': datetime.datetime(2017, 4, 16, 15, 41, 38, 613000),
#                                         'value': Decimal('0.00')
#                                     }
#                                 ],
#                                 'package_info_str': [
#                                     {
#                                         'id': -1L,
#                                         'inserted_on': datetime.datetime(2017, 4, 16, 15, 41, 38, 613000),
#                                         'name': 'NON_STANDARD',
#                                         'updated_on': datetime.datetime(2017, 4, 16, 15, 41, 38, 613000),
#                                         'value': 'TRUE'
#                                     },
#                                     {
#                                         'id': -1L,
#                                         'inserted_on': datetime.datetime(2017, 4, 16, 15, 41, 38, 613000),
#                                         'name': 'SPECIAL_HANDLING',
#                                         'updated_on': datetime.datetime(2017, 4, 16, 15, 41, 38, 613000),
#                                         'value': 'FALSE'
#                                     }
#                                 ],
#                                 'package_num': 0L,
#                                 'package_reference': 0L,
#                                 'reported_weight': Decimal('44.0'),
#                                 'updated_on': datetime.datetime(2017, 4, 16, 15, 41, 38, 613000)
#                             }
#                         ],
#                         'pickup_address_line_1': '12A - 3033 KING GEORGE BLVD.',
#                         'pickup_address_line_2': None,
#                         'pickup_address_line_3': None,
#                         'pickup_city': 'SURREY',
#                         'pickup_email': None,
#                         'pickup_extension': None,
#                         'pickup_name': 'KX WHEELS',
#                         'pickup_phone': None,
#                         'pickup_postal_code': 'V4P1B8',
#                         'pickup_province': 'BC',
#                         'proforma': {
#                             'broker_address_line_1': None,
#                             'broker_city': None,
#                             'broker_country': None,
#                             'broker_extension': None,
#                             'broker_name': None,
#                             'broker_phone': None,
#                             'broker_postal_code': None,
#                             'broker_province': None,
#                             'business_num': None,
#                             'currency_of_declared_value': None,
#                             'extension': None,
#                             'id': None,
#                             'inserted_on': None,
#                             'name': None,
#                             'permit_num': None,
#                             'phone': None,
#                             'proforma_items': [],
#                             'reason_for_export': None,
#                             'reference': None,
#                             'status': None,
#                             'updated_on': None
#                         },
#                         'reported_weight_unit': 'L',
#                         'service_type': 'DD',
#                         'shipment_info_num': [
#                             {
#                                 'id': -1L,
#                                 'inserted_on': datetime.datetime(2017, 4, 16, 15, 41, 38, 613000),
#                                 'name': 'DECLARED_VALUE',
#                                 'updated_on': datetime.datetime(2017, 4, 16, 15, 41, 38, 613000),
#                                 'value': Decimal('1600.00')
#                             },
#                             {
#                                 'id': -1L,
#                                 'inserted_on': datetime.datetime(2017, 4, 16, 15, 41, 38, 613000),
#                                 'name': 'BASE_CHARGE',
#                                 'updated_on': datetime.datetime(2017, 4, 16, 15, 41, 38, 613000),
#                                 'value': Decimal('12.65')
#                             },
#                             {
#                                 'id': -1L,
#                                 'inserted_on': datetime.datetime(2017, 4, 16, 15, 41, 38, 613000),
#                                 'name': 'ADD_SER_CHARGE',
#                                 'updated_on': datetime.datetime(2017, 4, 16, 15, 41, 38, 613000),
#                                 'value': Decimal('5.00')
#                             },
#                             {
#                                 'id': -1L,
#                                 'inserted_on': datetime.datetime(2017, 4, 16, 15, 41, 38, 613000),
#                                 'name': 'VALUATION_CHARGE',
#                                 'updated_on': datetime.datetime(2017, 4, 16, 15, 41, 38, 613000),
#                                 'value': Decimal('45.00')
#                             },
#                             {
#                                 'id': -1L,
#                                 'inserted_on': datetime.datetime(2017, 4, 16, 15, 41, 38, 613000),
#                                 'name': 'TOTAL_CHARGE',
#                                 'updated_on': datetime.datetime(2017, 4, 16, 15, 41, 38, 613000),
#                                 'value': Decimal('68.53')
#                             },
#                             {
#                                 'id': -1L,
#                                 'inserted_on': datetime.datetime(2017, 4, 16, 15, 41, 38, 613000),
#                                 'name': 'CHARGE_R',
#                                 'updated_on': datetime.datetime(2017, 4, 16, 15, 41, 38, 613000),
#                                 'value': Decimal('5.00')
#                             },
#                             {
#                                 'id': -1L,
#                                 'inserted_on': datetime.datetime(2017, 4, 16, 15, 41, 38, 613000),
#                                 'name': 'CUBIC_FACTOR',
#                                 'updated_on': datetime.datetime(2017, 4, 16, 15, 41, 38, 613000),
#                                 'value': Decimal('13.00')
#                             }
#                         ],
#                         'shipment_info_str': [
#                             {
#                                 'id': -1L,
#                                 'inserted_on': datetime.datetime(2017, 4, 16, 15, 41, 38, 613000),
#                                 'name': 'DANGEROUS_GOODS',
#                                 'updated_on': datetime.datetime(2017, 4, 16, 15, 41, 38, 613000),
#                                 'value': 'FALSE'
#                             },
#                             {
#                                 'id': -1L,
#                                 'inserted_on': datetime.datetime(2017, 4, 16, 15, 41, 38, 613000),
#                                 'name': 'REFERENCE',
#                                 'updated_on': datetime.datetime(2017, 4, 16, 15, 41, 38, 613000),
#                                 'value': 'AABBCC0928283'
#                             },
#                             {
#                                 'id': -1L,
#                                 'inserted_on': datetime.datetime(2017, 4, 16, 15, 41, 38, 613000),
#                                 'name': 'CODE',
#                                 'updated_on': datetime.datetime(2017, 4, 16, 15, 41, 38, 613000),
#                                 'value': 'AA'
#                             },
#                             {
#                                 'id': -1L,
#                                 'inserted_on': datetime.datetime(2017, 4, 16, 15, 41, 38, 613000),
#                                 'name': 'SERVICE_LABEL',
#                                 'updated_on': datetime.datetime(2017, 4, 16, 15, 41, 38, 613000),
#                                 'value': 'GRD'
#                             },
#                             {
#                                 'id': -1L,
#                                 'inserted_on': datetime.datetime(2017, 4, 16, 15, 41, 38, 613000),
#                                 'name': 'BRANCH_CITY',
#                                 'updated_on': datetime.datetime(2017, 4, 16, 15, 41, 38, 613000),
#                                 'value': 'BURNABY'
#                             }
#                         ],
#                         'shipment_status': 'R',
#                         'shipper_num': 'HB4499',
#                         'shipping_date': '20170416',
#                         'tax_charge_1': Decimal('3.26'),
#                         'tax_charge_2': Decimal('0.00'),
#                         'tax_code_1': 'GST',
#                         'tax_code_2': None,
#                         'transit_time': 1L,
#                         'transit_time_guaranteed': False,
#                         'updated_on': datetime.datetime(2017, 4, 16, 15, 41, 38, 613000),
#                         'user_id': 'ADMIN@USS.COM',
#                         'voided': False,
#                         'zone': 1L
#                     }
#                 }
#             ]
#         }
#
#
#     def tearDown(self):
#         pass
#
#     def test_connection(self):
#         shipper = Shipper(seller=self.seller, buyer=self.buyer, parcel=self.parcel)
#         shipper.fetch_response()
#
#         self.assertIsNone(shipper.response['error'])
#
#         products = shipper.products()
#         self.assertEquals(len(products), 1)
#
#         returned_rate = shipper.response.getRatesResult[0].shipment.shipment_info_num[4].value
#         self.assertEquals(products[0].rate, returned_rate)



class ShipmentTestMixin(object):
    def get_shipper(self):
        return Shipper(seller=self.seller,
                       buyer=self.buyer,
                       parcel=self.parcel,
                       service=self.service)

    def test_print_output(self):
        shipper = self.get_shipper()
        shipper.fetch_response()

        if self.debug:
            pp(shipper.request)
            print(shipper.response)

        print("Test name: {}\n---------".format(self.testname))
        print("Base charge: {}".format(shipper._get_base_charge()))
        print("Freight charge: {}".format(shipper._get_freight_charge()))
        print("Fuel surcharge: {}".format(shipper._get_fuel_surcharge()))
        print("Add ser charge: {}".format(shipper._get_add_ser_charge()))
        print("Tax charge 1: {}".format(shipper._get_tax_charge_1()))
        print("Tax charge 2: {}".format(shipper._get_tax_charge_2()))
        print("Total charge: {}".format(shipper._get_total_charge()))


# class ShipmentOneTestCase(ShipmentTestMixin, TestCase):
#     service = 'DD'
#     testname = "Shipment One Test"
#     debug = False
#
#     def setUp(self):
#         self.seller = seller
#
#         self.buyer = Buyer(name='LIVE CYCLE QUEBEC',
#                            address='1295 DE LA JONQUIERE',
#                            city='QUEBEC CITY',
#                            province='QC',
#                            postal_code='G1N2X2',
#                            country='CA',
#                            phone='5145551212',
#                            email='info@shiftonline.com', )
#
#         parcel_item = ParcelItem(name="Shipment 1 package",
#                                  qty=1,
#                                  unit_price="1",
#                                  weight=(10, 'lb'),
#                                  is_dangerous=True)
#
#         self.parcel = Parcel(items=[parcel_item, ])


class ShipmentTwoTestCase(ShipmentTestMixin, TestCase):
    service = 'DN'
    testname = "Shipment Two Test"
    debug = True

    def setUp(self):
        self.seller = seller

        self.buyer = Buyer(name='LIVE CYCLE CALGARY',
                           address='3000-15TH ST. N.E.',
                           city='CALGARY',
                           province='AB',
                           postal_code='T2E8V6',
                           country='CA',
                           phone='4035315967',
                           email='info@shiftonline.com', )

        parcel_item1 = ParcelItem(name="Shipment 1 package",
                                  qty=1,
                                  unit_price="400",
                                  weight=(10.9, 'lb'),
                                  length=(8, 'inch'),
                                  width=(8, 'inch'),
                                  height=(8, 'inch'))

        parcel_item2 = ParcelItem(name="Shipment 2 package",
                                  qty=1,
                                  unit_price="400",
                                  weight=(20.2, 'lb'),
                                  length=(12, 'inch'),
                                  width=(12, 'inch'),
                                  height=(12, 'inch'))

        parcel_item3 = ParcelItem(name="Shipment 3 package",
                                  qty=1,
                                  unit_price="400",
                                  weight=(15, 'lb'),)

        self.parcel = Parcel(items=[parcel_item1,
                                    parcel_item2,
                                    parcel_item3])
#
# class ShipmentThreeTestCase(ShipmentTestMixin, TestCase):
#     service = 'DE'
#     testname = "Shipment Three Test"
#     debug = True
#
#     def setUp(self):
#         self.seller = seller
#
#         self.buyer = Buyer(name='LIVE CYCLE MISSISSAUGA',
#                            address='90 MATHESON BLVD',
#                            city='MISSISSAUGA',
#                            province='ON',
#                            postal_code='L5R3R3',
#                            country='CA',
#                            phone='9055551212',
#                            email='info@shiftonline.com', )
#
#         parcel_item1 = ParcelItem(name="Shipment 1 package",
#                                   qty=1,
#                                   unit_price="0",
#                                   weight=(1.3, 'lb'))
#
#         parcel_item2 = ParcelItem(name="Shipment 2 package",
#                                   qty=4,
#                                   unit_price="0",
#                                   weight=(8.2, 'lb'),
#                                   length=(12, 'inch'),
#                                   width=(13, 'inch'),
#                                   height=(8, 'inch'))
#
#         parcel_item3 = ParcelItem(name="Shipment 3 package",
#                                   qty=5,
#                                   unit_price="0",
#                                   weight=(32.5, 'lb'),
#                                   length=(11, 'inch'),
#                                   width=(27, 'inch'),
#                                   height=(23, 'inch'))
#
#         self.parcel = Parcel(items=[parcel_item1,
#                                     parcel_item2,
#                                     parcel_item3])
#
#     def get_shipper(self):
#         return Shipper(seller=self.seller,
#                        buyer=self.buyer,
#                        parcel=self.parcel,
#                        service=self.service,
#                        collect_shipper_number='AB1234',
#                        is_saturday_delivery=True,
#                        is_residential=True)

# class ShipmentFourTestCase(ShipmentTestMixin, TestCase):
#     service = 'D9'
#     testname = "Shipment Four Test"
#     debug = True
#
#     def setUp(self):
#         self.seller = seller
#
#         self.buyer = Buyer(name='LIVE CYCLE DARTMOUTH',
#                            address='100 JOSEPH ZATZMAN',
#                            city='DARTMOUTH',
#                            province='NS',
#                            postal_code='B3B1N8',
#                            country='CA',
#                            phone='7054265584',
#                            email='info@shiftonline.com', )
#
#         parcel_item1 = ParcelItem(name="Shipment 1 package",
#                                   qty=1,
#                                   unit_price="0",
#                                   weight=(12.2, 'lb'))
#
#         parcel_item2 = ParcelItem(name="Shipment 2 package",
#                                   qty=1,
#                                   unit_price="0",
#                                   weight=(12.2, 'lb'),
#                                   length=(3, 'inch'),
#                                   width=(14, 'inch'),
#                                   height=(15, 'inch'))
#
#         parcel_item3 = ParcelItem(name="Shipment 3 package",
#                                   qty=1,
#                                   unit_price="0",
#                                   weight=(12.2, 'lb'))
#
#         self.parcel = Parcel(items=[parcel_item1,
#                                     parcel_item2,
#                                     parcel_item3],
#                              is_fragile=True)
#
#     def get_shipper(self):
#         return Shipper(seller=self.seller,
#                        buyer=self.buyer,
#                        parcel=self.parcel,
#                        service=self.service,
#                        is_nsr=True)
#
# class ShipmentFiveTestCase(ShipmentTestMixin, TestCase):
#     service = 'DD'
#     testname = "Shipment Five Test"
#     debug = False
#
#     def setUp(self):
#         self.seller = seller
#
#         self.buyer = Buyer(name='LIVE CYCLE MISSISSAUGA',
#                            address='90 MATHESON BLVD',
#                            city='MISSISSAUGA',
#                            province='ON',
#                            postal_code='L5R3R3',
#                            country='CA',
#                            phone='9055551212',
#                            email='info@shiftonline.com', )
#
#         parcel_item1 = ParcelItem(name="Shipment 1 package",
#                                   qty=1,
#                                   unit_price="0",
#                                   weight=(10, 'lb'),
#                                   length=(12, 'inch'),
#                                   width=(12, 'inch'),
#                                   height=(12, 'inch'))
#
#
#         parcel_item2 = ParcelItem(name="Shipment 2 package",
#                                   qty=1,
#                                   unit_price="0",
#                                   weight=(10.6, 'lb'),
#                                   length=(12, 'inch'),
#                                   width=(12, 'inch'),
#                                   height=(12, 'inch'))
#
#
#         self.parcel = Parcel(items=[parcel_item1,
#                                     parcel_item2],
#                              is_fragile=True)
#
#     def get_shipper(self):
#         return Shipper(seller=self.seller,
#                        buyer=self.buyer,
#                        parcel=self.parcel,
#                        service=self.service,
#                        is_saturday_delivery=True,
#                        is_residential=True)

# #
# class ShipmentSixTestCase(ShipmentTestMixin, TestCase):
#     service = 'DE'
#     testname = "Shipment Six Test"
#     debug = False
#
#     def setUp(self):
#         self.seller = seller
#
#         self.buyer = Buyer(name='LIVE CYCLE SASKATOON',
#                            address='2519 KOYL AVE',
#                            city='SASKATOON',
#                            province='SK',
#                            postal_code='S7L5X8',
#                            country='CA',
#                            phone='3063435339',
#                            email='info@shiftonline.com', )
#
#         parcel_item1 = ParcelItem(name="Shipment 1 package",
#                                   qty=1,
#                                   unit_price="0",
#                                   weight=(10.9, 'lb'),
#                                   length=(8, 'inch'),
#                                   width=(8, 'inch'),
#                                   height=(8, 'inch'))
#
#
#         parcel_item2 = ParcelItem(name="Shipment 2 package",
#                                   qty=1,
#                                   unit_price="0",
#                                   weight=(15.1, 'lb'),
#                                   length=(12, 'inch'),
#                                   width=(12, 'inch'),
#                                   height=(12, 'inch'))
#
#         parcel_item3 = ParcelItem(name="Shipment 3 package",
#                                   qty=1,
#                                   unit_price="0",
#                                   weight=(20.2, 'lb'),
#                                   length=(12, 'inch'),
#                                   width=(12, 'inch'),
#                                   height=(12, 'inch'))
#
#         self.parcel = Parcel(items=[parcel_item1,
#                                     parcel_item2,
#                                     parcel_item3])
#
# class ShipmentSevenTestCase(ShipmentTestMixin, TestCase):
#     service = 'D9'
#     testname = "Shipment Seven Test"
#     debug = False
#
#     def setUp(self):
#         self.seller = seller
#
#         self.buyer = Buyer(name='LIVE CYCLE RICHMOND',
#                            address='101-5000 MILLER ROAD',
#                            city='RICHMOND',
#                            province='BC',
#                            postal_code='V7B1K6',
#                            country='CA',
#                            phone='6046656510',
#                            email='info@shiftonline.com', )
#
#         parcel_item1 = ParcelItem(name="Shipment 1 package",
#                                   qty=1,
#                                   unit_price="1",
#                                   weight=(40.5, 'lb'),
#                                   length=(24, 'inch'),
#                                   width=(32, 'inch'),
#                                   height=(25, 'inch'))
#
#
#         parcel_item2 = ParcelItem(name="Shipment 2 package",
#                                   qty=1,
#                                   unit_price="1",
#                                   weight=(40.5, 'lb'),
#                                   length=(24, 'inch'),
#                                   width=(32, 'inch'),
#                                   height=(25, 'inch'))
#
#
#         self.parcel = Parcel(items=[parcel_item1,
#                                     parcel_item2])
#
#
#     def get_shipper(self):
#         return Shipper(seller=self.seller,
#                        buyer=self.buyer,
#                        parcel=self.parcel,
#                        service=self.service,
#                        collect_shipper_number='FG7417')
# #
# class ShipmentEightTestCase(ShipmentTestMixin, TestCase):
#     service = 'DD'
#     testname = "Shipment Eight Test"
#     debug = False
#
#     def setUp(self):
#         self.seller = seller
#
#         self.buyer = Buyer(name='LIVE CYCLE RICHMOND',
#                            address='101-5000 MILLER ROAD',
#                            city='RICHMOND',
#                            province='BC',
#                            postal_code='V7B1K6',
#                            country='CA',
#                            phone='6046656510',
#                            email='info@shiftonline.com', )
#
#         parcel_item1 = ParcelItem(name="Shipment 1 package",
#                                   qty=1,
#                                   unit_price="1",
#                                   weight=(30.5, 'lb'),
#                                   length=(24, 'inch'),
#                                   width=(32, 'inch'),
#                                   height=(25, 'inch'))
#
#
#         parcel_item2 = ParcelItem(name="Shipment 2 package",
#                                   qty=1,
#                                   unit_price="1",
#                                   weight=(30.5, 'lb'),
#                                   length=(24, 'inch'),
#                                   width=(32, 'inch'),
#                                   height=(25, 'inch'))
#
#
#         self.parcel = Parcel(items=[parcel_item1,
#                                     parcel_item2])
#
#
# class ShipmentNineTestCase(ShipmentTestMixin, TestCase):
#     service = 'DD'
#     testname = "Shipment Nine Test"
#     debug = False
#
#     def setUp(self):
#         self.seller = seller
#
#         self.buyer = Buyer(name='LOOMIS EXPRESS IT',
#                            address='5425 DIXIE RD',
#                            address_line_2='ATTN: MSS DEPARTMENT',
#                            city='MISSISSAUGA',
#                            province='ON',
#                            postal_code='L4W1E6',
#                            country='CA',
#                            phone='9054528759',
#                            email='info@shiftonline.com', )
#
#         parcel_item1 = ParcelItem(name="Shipment 1 package",
#                                   qty=1,
#                                   unit_price="1",
#                                   weight=(0.9, 'lb'))
#
#         self.parcel = Parcel(items=[parcel_item1])
# #

from django.test import TestCase
from kxwheels.apps.vehicle.models import *

class VehicleTestCase(TestCase):
    fixtures = ['vehicle/fixtures/sample_data.json',]
    
    def testModel(self):
        tl_2008 = Model.objects.get(name='TL', year=2008)
        
        self.assertEquals(tl_2008.slug, 'tl-2008')
        self.assertEquals(tl_2008.boltpattern, '5x120')
        
        self.assertEquals(tl_2008.has_front_wheel_size, True)
        self.assertEquals(tl_2008.has_rear_wheel_size, False)
        self.assertEquals(tl_2008.has_oe_tire_sizes, True)
        self.assertEquals(tl_2008.has_oe_staggered_tire_sizes, False)
        self.assertEquals(tl_2008.has_plus_tire_sizes, True)
        self.assertEquals(tl_2008.has_plus_staggered_tire_sizes, False)
        
        # Front wheel size
        self.assertEquals(tl_2008.front_wheel_size.diameter_range, '17,22')
        self.assertEquals(tl_2008.front_wheel_size.wheelwidth_range, '7.5,8.5')
        self.assertEquals(tl_2008.front_wheel_size.offset_range, '35,45')
        
        # OE tire sizes
        _oe_tire_sizes = tl_2008.oe_tire_sizes.all()
        self.assertEquals(_oe_tire_sizes[0].treadwidth, '245')
        self.assertEquals(_oe_tire_sizes[0].profile, '50')
        self.assertEquals(_oe_tire_sizes[0].diameter, '17')
        self.assertEquals(_oe_tire_sizes[1].treadwidth, '245')
        self.assertEquals(_oe_tire_sizes[1].profile, '45')
        self.assertEquals(_oe_tire_sizes[1].diameter, '18')
        self.assertEquals(_oe_tire_sizes[2].treadwidth, '245')
        self.assertEquals(_oe_tire_sizes[2].profile, '45')
        self.assertEquals(_oe_tire_sizes[2].diameter, '19')
        
        
        
        
        
                

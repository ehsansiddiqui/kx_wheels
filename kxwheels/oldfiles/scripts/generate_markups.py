
from apps.kx.models.wheel import DealerWheelManufacturerDiscount, WheelManufacturer
from apps.kx.models.tire import DealerTireManufacturerDiscount, TireManufacturer

from django.contrib.admin.models import User

wh = WheelManufacturer.objects.all()
th = TireManufacturer.objects.all()
for u in User.objects.filter(profiles__subdomain__isnull=False):

    for m in th:
        tire_markups = DealerTireManufacturerDiscount.objects.filter(user=u, manufacturer=m)
        if not len(tire_markups):
            print 'adding', u,m
            d = DealerTireManufacturerDiscount(
                user=u,
                manufacturer=m,
                discount=25
            )
            d.save()
            
    for m in wh:
        markups = DealerWheelManufacturerDiscount.objects.filter(user=u, manufacturer=m)
        if not len(markups):
            print 'adding', u,m
            d = DealerWheelManufacturerDiscount(
                user=u,
                manufacturer=m,
                discount=25
            )
            d.save()
            
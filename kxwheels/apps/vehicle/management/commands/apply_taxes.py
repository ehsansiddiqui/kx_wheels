import os
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    args = '<source ...>'
    help = 'Imports TPMS data from the specified CSV file.'

    def handle(self, *args, **options):
        
        print "Applying tax..."

        from kxwheels.apps.shop.models import TaxClass
        from kxwheels.apps.kx.models import TireSize, WheelSize
        from kxwheels.apps.vehicle.models import TPMS

        hst = TaxClass.objects.get(name="HST")
        gst = TaxClass.objects.get(name="GST + (PST-BC Only)")
        levy = TaxClass.objects.get(name="Levy")

        tss = TireSize.objects.all()
        wss = WheelSize.objects.all()
        tpmss = TPMS.objects.all()

        # for ts in tss:
        #     ts.tax.add(gst)
        #     ts.tax.add(levy)
        #     ts.tax.add(hst)

        for ws in wss:
            ws.tax.add(gst)
            ws.tax.add(hst)

        # for tpms in tpmss:
        #     tpms.tax.add(gst)
        #     tpms.tax.add(levy)
        print('Done.')


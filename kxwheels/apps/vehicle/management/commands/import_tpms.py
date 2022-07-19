import os
import csv
from random import randint
from django.core.management.base import BaseCommand, CommandError

from kxwheels.apps.vehicle.models import TPMS
from kxwheels.apps.vehicle.models import Manufacturer, Model

class Command(BaseCommand):
    args = '<source ...>'
    help = 'Imports TPMS data from the specified CSV file.'

    VALID_COLUMNS = (
        'year',
        'make',
        'model',
        'sensor',
        'price'
    )

    def handle(self, *args, **options):
        source = args[0]
        # Check if source exists
        if not os.path.isfile(source):
            raise CommandError('Source file does not exist')

        rows = self.parse(source)
        for i, row in enumerate(rows):
            print "Processing row %s" % i

            try:
                year = row.get('year')[0].strip()
            except IndexError:
                year = None

            try:
                make = row.get('make')[0].strip()
            except IndexError:
                make = None

            try:
                model = row.get('model')[0].strip()
            except IndexError:
                model = None

            try:
                sensor = row.get('sensor')[0].strip()
            except IndexError:
                sensor = None

            try:
                price = row.get('price')[0].strip()
            except IndexError:
                price = None

            if None in [year, make, model, sensor, price]:
                continue

            try:
                model = Model.objects.get(
                    year=year,
                    manufacturer__name=make,
                    name=model,
                )
            except Model.DoesNotExist:
                continue

            make = model.manufacturer

            # Model
            '''
            tpms, created = TPMS.objects.get_or_create(
                vehicle=model,
                sensor=sensor,
                price=price,
            )
            '''

            try:
                tpms = TPMS.objects.get(vehicle=model)
            except TPMS.DoesNotExist:
                tpms = TPMS.objects.create(
                    vehicle=model,
                    sensor=sensor,
                    price=price,
                )
            
            tpms.sku = "tpms%s" % randint(100000, 999999)
            tpms.name = "Tire Pressure Monitoring System - %s" % sensor
            tpms.weight = "0.00"
            tpms.quantity = 0
            tpms.save()

        print('Done.')

    def parse(self, source):
        with open(source, 'rU') as data:
            datadict = {}
            rows = csv.reader(data)
            fieldnames = rows.next()

            if set(self.VALID_COLUMNS).difference(set(fieldnames)):
                print set(self.VALID_COLUMNS).difference(set(fieldnames))
                raise CommandError("Fields don't match headings. Check it out!")

            mappings = dict((c, []) for c in self.VALID_COLUMNS)
            for i, fieldname in enumerate(fieldnames):
                mappings[fieldname].append(i)

            data = []
            for row in rows:
                itemdict = {}
                for key, value in mappings.items():
                    itemvalue = []
                    for v in value:
                        if row[v]: itemvalue.append(row[v])
                    itemdict[key] = itemvalue
                data.append(itemdict)

            return data

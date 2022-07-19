import os
import re
import csv
import time
from django.core.management.base import BaseCommand, CommandError
from kxwheels.apps.vehicle.models import *

class Command(BaseCommand):
    args = '<source ...>'
    help = 'Imports vechicle data from the specified CSV file.'

    VALID_COLUMNS = (
        'year',
        'manufacturer',
        'model',
        'boltpattern',
        'centerbore',
        'front_wheelsize',
        'rear_wheelsize',
        'oe_tiresize',
        'oe_staggered_tiresize',
        'plus_tiresize',
        'plus_staggered_tiresize',
    )

    def handle(self, *args, **options):
        source = args[0]
        # Check if source exists
        if not os.path.isfile(source):
            raise CommandError('Source file does not exist')

        rows = self.parse(source)
        fsock = open('debug.txt', 'wb')
        for i, row in enumerate(rows):
            print "Processing row %s" % i
            row_time = 0.00
            
            # Manufacturer
            start_time = time.time()
            manufacturer, created = Manufacturer.objects.get_or_create(
                name=row.get('manufacturer')[0].strip()
            )
            if created:
                manufacturer.save()
            exe_time = time.time() - start_time
            row_time += exe_time
            #print "Manufacturer: %s seconds" % exe_time

            # Model
            start_time = time.time()
            try:
                model, created = Model.objects.get_or_create(
                    manufacturer=manufacturer,
                    name=row.get('model')[0].strip(),
                    year=row.get('year')[0].strip(),
                    boltpattern=row.get('boltpattern')[0],
                    centerbore=row.get('centerbore')[0],
                )
            except:
                pass
            else:
                if created:
                    model.save()
            exe_time = time.time() - start_time
            row_time += exe_time
            #print "Model: %s seconds" % exe_time
            
            # Front wheel size
            start_time = time.time()
            try: fws = row.get('front_wheelsize')[0]
            except: fws = None
            if fws is not None:
                try:
                    _elements = fws.split(':')
                    front_wheel_size, created = FrontWheelSize.objects.get_or_create(
                        model=model,
                        diameter_range=_elements[2],
                        wheelwidth_range=_elements[1],
                        offset_range=_elements[0],
                    )
                    if created:
                        front_wheel_size.save()
                except Exception as e:
                    pass

            exe_time = time.time() - start_time
            row_time += exe_time
            #print "Front wheel size: %s seconds" % exe_time
                    
            # Rear wheel size
            start_time = time.time()
            try: rws = row.get('rear_wheelsize')[0]
            except: rws = None
            if rws is not None:
                _elements = rws.split(':')
                try:
                    rear_wheel_size, created = RearWheelSize.objects.get_or_create(
                        model=model,
                        diameter_range=_elements[2],
                        wheelwidth_range=_elements[1],
                        offset_range=_elements[0],
                    )
                    if created:
                        rear_wheel_size.save()
                except Exception as e:
                    pass
                
            exe_time = time.time() - start_time
            row_time += exe_time
            #print "Rear wheel size: %s seconds" % exe_time

            # OE tire size
            start_time = time.time()
            try: oets = row.get('oe_tiresize')
            except: oets = None
            if oets is not None:
                for ts in oets:
                    try:
                        _elements = map(lambda s: s.lower().strip(), ts.split(','))
                        if len(_elements) == 4:
                            _elements.insert(0, '')
                        oe_tire_size, created = OETireSize.objects.get_or_create(
                            model=model,
                            prefix=_elements[0],
                            treadwidth=_elements[1],
                            profile=_elements[2],
                            additional_size=_elements[3],
                            diameter=_elements[4],
                        )
                        if created:
                            oe_tire_size.save()
                    except Exception as e:
                        pass
            exe_time = time.time() - start_time
            row_time += exe_time
            #print "OE tire size: %s seconds" % exe_time
            
            # OE staggered tire size
            start_time = time.time()
            try:
                oests = row.get('oe_staggered_tiresize')
            except:
                oests = None

            if oests is not None:
                for sts in oests:
                    try:
                        ts = sts.split(':')
                        _front_ts = map(lambda s: s.lower().strip(), ts[0].split(','))
                        _rear_ts = map(lambda s: s.lower().strip(), ts[1].split(','))

                        if len(_front_ts) == 4:
                            _front_ts.insert(0, '')

                        if len(_rear_ts) == 4:
                            _rear_ts.insert(0, '')

                        oe_staggered_tire_size, created = OEStaggeredTireSize.objects.get_or_create(
                            model=model,
                            front_prefix=_front_ts[0],
                            front_treadwidth=_front_ts[1],
                            front_profile=_front_ts[2],
                            front_additional_size=_front_ts[3],
                            front_diameter=_front_ts[4],

                            rear_prefix=_rear_ts[0],
                            rear_treadwidth=_rear_ts[1],
                            rear_profile=_rear_ts[2],
                            rear_additional_size=_rear_ts[3],
                            rear_diameter=_rear_ts[4],
                        )
                        if created:
                            oe_staggered_tire_size.save()
                    except Exception as e:
                        pass
                        
            exe_time = time.time() - start_time
            row_time += exe_time
            #print "OE staggered size: %s seconds" % exe_time
            
            # Plus tire size
            start_time = time.time()
            try:
                pts = row.get('plus_tiresize')
            except:
                pts = None

            if pts is not None:
                for ts in pts:
                    try:
                        _elements = map(lambda s: s.lower().strip(), ts.split(','))

                        if len(_elements) == 4:
                            _elements.insert(0, '')

                        plus_tire_size, created = PlusTireSize.objects.get_or_create(
                            model=model,
                            prefix=_elements[0],
                            treadwidth=_elements[1],
                            profile=_elements[2],
                            additional_size=_elements[3],
                            diameter=_elements[4],
                        )
                        if created:
                            plus_tire_size.save()
                    except Exception as e:
                        pass

            exe_time = time.time() - start_time
            row_time += exe_time
            #print "Plus tire size: %s seconds" % exe_time
            
            # Plus staggered tire size
            start_time = time.time()
            try:
                psts = row.get('plus_staggered_tiresize')
            except:
                psts = None

            if psts is not None:
                for pts in psts:
                    try:
                        ts = pts.split(':')
                        _front_ts = map(lambda s: s.lower().strip(), ts[0].split(','))
                        _rear_ts = map(lambda s: s.lower().strip(), ts[1].split(','))

                        if len(_front_ts) == 4:
                            _front_ts.insert(0, '')

                        if len(_rear_ts) == 4:
                            _rear_ts.insert(0, '')

                        plus_staggered_tire_size, created = PlusStaggeredTireSize.objects.get_or_create(
                            model=model,
                            front_prefix=_front_ts[0],
                            front_treadwidth=_front_ts[1],
                            front_profile=_front_ts[2],
                            front_additional_size=_front_ts[3],
                            front_diameter=_front_ts[4],

                            rear_prefix=_rear_ts[0],
                            rear_treadwidth=_rear_ts[1],
                            rear_profile=_rear_ts[2],
                            rear_additional_size=_rear_ts[3],
                            rear_diameter=_rear_ts[4],
                        )
                        if created:
                            plus_staggered_tire_size.save()
                    except Exception as e:
                        pass

            exe_time = time.time() - start_time
            row_time += exe_time
            #print "Plus staggered size: %s seconds" % exe_time
            
            print "Finished row %s in %s" % (i, row_time)
            print "-"*10
            fsock.write(str(row_time) + "\n")
                        
        print('Done.')
        fsock.close()

    def parse(self, source):
        with open(source, 'rU') as data:
            datadict = {}
            rows = csv.reader(data)
            fieldnames = rows.next()
            
            #headings = map(lambda title: title.lower().strip(), fieldnames)
            #if (fieldnames != headings):
            print set(self.VALID_COLUMNS).difference(set(fieldnames))
            if set(self.VALID_COLUMNS).difference(set(fieldnames)):
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
        
    
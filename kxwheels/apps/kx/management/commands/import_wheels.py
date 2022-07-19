import os
import re
import csv
import time
from time import sleep
from django.core.management.base import BaseCommand, CommandError
from kxwheels.apps.kx.models.wheel import *
from django.core.files import File
from boto.s3.connection import S3Connection
import urllib
from kxwheels.apps.shop.models.tax import *


class Command(BaseCommand):

    args = '<source ...>'
    help = 'Imports vechicle data from the specified CSV file.'

    VALID_COLUMNS = (
        'manufacturer',
        'wheel',
        'finish',
        'diameter',
        'wheelwidth',
        'boltpattern_1',
        'boltpattern_2',
        'offset',
        'centerbore',
        'availability',
        'sku',
        'quantity',
        'price',
        'weight',
        'picture_1',
        'picture_2',
        'picture_3',
        'picture_4',
        'meta_keywords',
        'meta_description',
        'description',
    )

    def handle(self, *args, **options):
        wheels_name = []
        source = args[0]
        # print "in Hnadle"
        # Check if source exists
        if not os.path.isfile(source):
            raise CommandError('Source file does not exist')
        # try:
        #     conn = S3Connection('AKIAJ3NVRT46U3FJB7GA', 'AcXHv68WRH806hSQd5sqy0cb54I56404bmTIN9AH')
        #     print "----------"
        #     print conn
        #     print "----------"
        # except Exception as e:
        #     print "in exc"
        #     print e
        # bucket = conn.get_bucket('kxwheels')
        # bucket_list = bucket.list(prefix='Brands/Fuel Offroad Wheels/')
        # for key in bucket_list:
        #     folders = key.name.encode('utf-8')
        #     # print folders

        rows = self.parse(source)
        fsock = open('debug.txt', 'wb')
        ids_arr = []
        name_arr = []
        brand_arr = []        
        try:
            hst=0
            gst=0
            # if hst is None:
            #     b=TaxClass(id='0')
            #     b.save()
            
            hst = TaxClass.objects.get(name="HST")
            gst = TaxClass.objects.get(name="GST + (PST-BC Only)")
        except Exception as e:
            print e.message
        
        for i, row in enumerate(rows):
            if row.get('wheel')[0].strip() not in name_arr:
                name_arr.append(row.get('wheel')[0].strip())
            try:
                row.get('manufacturer')[0].strip()
                if row.get('manufacturer')[0].strip() not in brand_arr:
                    brand_arr.append(row.get('manufacturer')[0].strip())
            except:
                continue
        try:
            for brand in brand_arr:
                brands = WheelManufacturer.objects.get(name=brand)
                wheels = Wheel.objects.filter(manufacturer=brands.id)
                for wheel in wheels:
                    if wheel.name not in name_arr:
                        ids_arr.append(wheel.id)
                if len(ids_arr) > 0:
                    WheelPicture.objects.filter(wheel__in=ids_arr).delete()
                    WheelSize.objects.filter(wheel__in=ids_arr).delete()
                    Wheel.objects.filter(id__in=ids_arr).delete()
        except Exception as e:
            pass
        for i, row in enumerate(rows):
            print "Processing row %s" % i
            row_time = 0.00

            # Manufacturer
            start_time = time.time()
            try:
                row.get('manufacturer')[0].strip()
                try:
                    row.get('meta_keywords')[0].strip()
                except:
                    continue
            except:
                continue
            try:
                manufacturer = WheelManufacturer.objects.get(
                    name=row.get('manufacturer')[0].strip(),
                )
                manufacturer.meta_keywords = row.get('meta_keywords')[0].strip(),
                manufacturer.meta_description = row.get('meta_description')[0].strip(),
                manufacturer.save()
            except WheelManufacturer.DoesNotExist:
                manufacturer = WheelManufacturer(
                    name=row.get('manufacturer')[0].strip(),
                    meta_keywords=row.get('meta_keywords')[0].strip(),
                    meta_description=row.get('meta_description')[0].strip(),
                    picture= File(open('static/img/accord_honda_2013_wheel_lg.jpg','r'))
                )

                manufacturer.save()
            exe_time = time.time() - start_time
            row_time += exe_time
            # print "Manufacturer: %s seconds" % exe_time

            # Wheel
            start_time = time.time()
            try:
                wheel = Wheel.objects.get(
                    manufacturer=manufacturer,
                    name=row.get('wheel')[0].strip(),
                )
                wheel.meta_keywords = row.get('meta_keywords')[0].strip()
                wheel.meta_description = row.get('meta_description')[0].strip()
                wheel.description = row.get('description')[0].strip()
                wheel.save()
            except Wheel.DoesNotExist:
                wheel = Wheel(
                    manufacturer=manufacturer,
                    meta_keywords=row.get('meta_keywords')[0].strip(),
                    meta_description=row.get('meta_description')[0].strip(),
                    name=row.get('wheel')[0].strip(),
                    description=row.get('description')[0].strip(),
                )
                wheel.save()
            exe_time = time.time() - start_time
            row_time += exe_time

            # WheelPicture
            start_time = time.time()
            try:
                wheel_picture = WheelPicture.objects.get(
                    wheel=wheel,
                )
                try:
                    wheel_name =  row.get('wheel')[0].strip()
                    manufacturrer = row.get('manufacturer')[0].replace(' ', '+')
                    bucket = conn.get_bucket('kxwheels')
                    bucket_list = bucket.list(prefix='Brands/'+row.get('manufacturer')[0].strip()+'/')
                    for key in bucket_list:
                        folders = key.name.encode('utf-8').split('/')
                        img_name = folders[2].split('.')[0]
                        if wheel_name in wheels_name:
                            pass
                        else:
                            if img_name == wheel_name:
                                urllib.urlretrieve(
                                    "https://s3.amazonaws.com/kxwheels/Brands/" + manufacturrer + "/" + img_name.replace(
                                        ' ', '+') + ".jpeg ", "static/scrapped_images/" + img_name.replace(
                                        ' ', '+') + ".jpeg ")

                                print "https://s3.amazonaws.com/kxwheels/Brands/" + manufacturrer + "/" + img_name.replace(
                                        ' ', '+') + ".jpeg "
                                file = "static/scrapped_images/" + img_name.replace(
                                    ' ', '+') + ".jpeg "
                                wheel_picture.picture = File(open(file, 'r'))
                                wheel_picture.save()
                                wheels_name.append(wheel_name)

                            else:
                                pass

                except Exception as e:
                    pass
            except WheelPicture.DoesNotExist:
                try:
                    wheel_name = row.get('wheel')[0].strip()
                    manufacturrer = row.get('manufacturer')[0].replace(' ', '+')
                    bucket = conn.get_bucket('kxwheels')
                    bucket_list = bucket.list(prefix='Brands/' + row.get('manufacturer')[0].strip() + '/')
                    for key in bucket_list:
                        folders = key.name.encode('utf-8').split('/')
                        img_name = folders[2].split('.')[0]
                        if wheel_name in wheels_name:
                            pass
                        else:
                            if img_name == wheel_name:
                                urllib.urlretrieve(
                                    "https://s3.amazonaws.com/kxwheels/Brands/" + manufacturrer + "/" + img_name.replace(
                                        ' ', '+') + ".jpeg ", "static/scrapped_images/" + img_name.replace(
                                        ' ', '+') + ".jpeg ")
                                file = "static/scrapped_images/" + img_name.replace(
                                    ' ', '+') + ".jpeg "
                                wheel_picture = WheelPicture(
                                        wheel=wheel,
                                        picture=File(open(file, 'r'))
                                    )
                                wheel_picture.save()
                                wheels_name.append(wheel_name)
                            else:
                                # wheels_name.append(wheel_name)
                                pass
                # try:
                #     wheel_scrapped_picture = WheelScrappedPictures.objects.get(part_no="{}".format(row.get('sku')[0].strip()))
                #     img_name = wheel_scrapped_picture.pic_url.split('/')[-1].split('.')[0]
                #     if ' ' in wheel_scrapped_picture.pic_url:
                #         urllib.urlretrieve(wheel_scrapped_picture.pic_url, "static/scrapped_images/"+wheel_scrapped_picture.pic_url.split('/')[-1].replace(" ", "-"))
                #         img_2 = "static/scrapped_images/"+wheel_scrapped_picture.pic_url.split('/')[-1].replace(" ", "-")
                #     elif '&' in wheel_scrapped_picture.pic_url:
                #         urllib.urlretrieve(wheel_scrapped_picture.pic_url, "static/scrapped_images/"+wheel_scrapped_picture.pic_url.split('/')[-1].replace("&", "-"))
                #         img_2 = "static/scrapped_images/"+wheel_scrapped_picture.pic_url.split('/')[-1].replace("&", "-")
                #     else:
                #         img_2 = wheel_scrapped_picture.pic_url
                #     os.system("convert "+img_2+" -resize 300x300 -size 300x300 xc:white +swap -compose over -composite static/scrapped_images/"+img_name.replace(' ', '-').replace('&', '-')+".jpg &")
                #     sleep(4)
                #     file = "static/scrapped_images/"+img_name.replace(' ', '-').replace('&', '-')+".jpg"
                except Exception:
                    pass

            exe_time = time.time() - start_time
            row_time += exe_time

            # WheelSize
            start_time = time.time()
            try:
                boltpattern_2 = row.get('boltpattern_2')[0].strip()
            except:
                boltpattern_2 = ''
            try:
                boltpattern_1 = row.get('boltpattern_1')[0].strip()
            except:
                boltpattern_1 = ''
            try:
                centerbore = row.get('centerbore')[0].strip()
            except:
                centerbore = ''
            try:
                offset = int(row.get('offset')[0].strip())
            except:
                offset = 0
            try:
                finish = row.get('finish')[0].strip()
            except:
                finish = ''
            try:
                sku = row.get('sku')[0].strip()
            except:
                sku = ''
            try:
                wheel_size = WheelSize.objects.get(
                    wheel=wheel,
                    sku=sku,
                )
                wheel_size.quantity = row.get('quantity')[0].strip()
                wheel_size.price = row.get('price')[0].strip()
                wheel_size.meta_keywords = row.get('meta_keywords')[0].strip()
                wheel_size.meta_description = row.get('meta_description')[0].strip()
                wheel_size.weight = row.get('weight')[0].strip()
                wheel_size.wheelwidth = float(row.get('wheelwidth')[0].strip())
                wheel_size.diameter = row.get('diameter')[0].strip()
                wheel_size.offset = offset
                wheel_size.finish = finish
                wheel_size.boltpattern_1 = boltpattern_1
                wheel_size.boltpattern_2 = boltpattern_2
                wheel_size.centerbore = centerbore
                wheel_size.tax.add(hst)
                wheel_size.tax.add(gst)
                wheel_size.availability = row.get('availability')[0].strip()
                wheel_size.save()
            except WheelSize.DoesNotExist:
                wheel_size = WheelSize(
                    wheel=wheel,
                    sku=sku,
                    quantity=row.get('quantity')[0].strip(),
                    price=row.get('price')[0].strip(),
                    meta_keywords=row.get('meta_keywords')[0].strip(),
                    meta_description=row.get('meta_description')[0].strip(),
                    weight=row.get('weight')[0].strip(),
                    wheelwidth=float(row.get('wheelwidth')[0].strip()),
                    diameter=row.get('diameter')[0].strip(),
                    offset=offset,
                    finish=finish,
                    boltpattern_1=boltpattern_1,
                    boltpattern_2=boltpattern_2,
                    centerbore=centerbore,
                    availability=row.get('availability')[0].strip(),
                )
                wheel_size.save()
                wheel_size.tax.add(hst)
                wheel_size.tax.add(gst)
            exe_time = time.time() - start_time
            row_time += exe_time

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
                if fieldname:
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

    def check_img_exist(self, img):
        try:
            img = WheelPicture.objects.filter(picture=img)
            return True
        except WheelPicture.DoesNotExist:
            return  False

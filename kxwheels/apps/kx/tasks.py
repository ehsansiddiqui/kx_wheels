import csv
import logging
from django.db import transaction
from re import sub
# from celery.task import task
from decimal import Decimal, InvalidOperation
from kxwheels.apps.kx.models import (Task,
                                     TireManufacturer,
                                     TireCategory,
                                     Tire,
                                     TireSize,
                                     TirePicture,
                                     WheelManufacturer,
                                     Wheel,
                                     WheelSize,
                                     WheelPicture)

import_logger = logging.getLogger('project.import')
errors = []


# @task
def import_tires(filepath, model='tire'):
    def clean(row):
        errors = []

        # Fields that are not required to be filled.
        NULL_FIELDS = ["utgq_rating", "ply", "prefix", "speed_rating", "sidewall_style",
                       "load_rating", "availability", "quantity", "weight",
                       "picture_1", "picture_2", "picture_3", "picture_4",
                       "meta_keywords", "meta_description", "description"]

        # Check if there are any fields that are required but have value missing
        for item in row.keys():
            if row[item]:
                row[item] = str(row[item]).strip()
            else:
                required_but_missing_fields = []

                if item not in NULL_FIELDS:
                    required_but_missing_fields.append(item.title())

                if required_but_missing_fields:
                    error = "Field(s) ({0}) missing in SKU {1}.".format(
                        ",".join(required_but_missing_fields), row['sku'])
                    errors.append(error)

        # Make all field values unicode
        for f in row.keys():
            try:
                row[f] = unicode(row[f], errors='replace')
            except TypeError:
                row[f] = unicode(str(row[f]), errors='replace')

        # Capitalize prefix
        row['prefix'] = row['prefix'].upper()

        # Set default weight
        if not row['weight']:
            row['weight'] = 20
        else:
            row['weight'] = int(row['weight'])
        row['weight_unit'] = 'lb'

        # Check quantity
        if not row['quantity']:
            row['quantity'] = 0

        # Fix the thumbnail paths
        for i in range(1, 5):
            if row['picture_%s' % i]:
                row['picture_%s' % i] = "media/tires/" + row['picture_%s' % i]
            else:
                row['picture_%s' % i] = None

        # Check price
        try:
            row['price'] = Decimal(sub(r'[^\d.]', '', row['price']))
        except InvalidOperation:
            errors.append("Invalid value for price ({0}) for SKU ({1})".format(
                row['price'], row['sku']))

        return row, errors

    def process(row, skudict):
        # TireManufacturer
        manufacturer, is_created = TireManufacturer.objects.get_or_create(
            name=row.get('manufacturer')
        )
        if is_created: manufacturer.save()
        row['manufacturer'] = manufacturer

        # TireCategory
        category, is_created = TireCategory.objects.get_or_create(
            name=row.get('category')
        )
        if is_created: category.save()
        row['category'] = category

        # Tire
        tire, is_created = Tire.objects.get_or_create(
            manufacturer=row.get('manufacturer'),
            category=row.get('category'),
            name=row.get('tire')
        )
        if is_created:
            tire.meta_keywords = row.get('meta_keywords')
            tire.meta_description = row.get('meta_description')
            tire.description = row.get('description')
            tire.save()

        row['tire'] = tire

        # Tire Pictures
        for i in range(1, 5):
            picture = row.get('picture_%s' % i, None)
            if picture:
                tirepicture, is_created = TirePicture.objects.get_or_create(
                    tire=tire,
                    picture=picture
                )
                tirepicture.save()

        # Tire Size
        tiresize_dict = row.copy()
        del (tiresize_dict['manufacturer'])
        del (tiresize_dict['category'])

        for i in range(1, 5):
            del (tiresize_dict['picture_%s' % i])

        del (tiresize_dict['meta_keywords'])
        del (tiresize_dict['meta_description'])
        del (tiresize_dict['description'])

        sku = row.get('sku').strip()
        if skudict.get(sku):
            import_logger.error("Duplicate products with the same sku found. The second one skipped. %s" % str(row))
            return skudict
        else:
            skudict[sku] = True

        try:
            tiresize = TireSize.objects.get(sku=sku)
        except TireSize.DoesNotExist:
            tiresize = TireSize.objects.create(**tiresize_dict)
        else:
            for field in tiresize_dict:
                setattr(tiresize, field, tiresize_dict.get(field))
        try:
            tiresize.save()
        except:
            import_logger.error("Error saving the row: %s" % str(row))

        return skudict

    # Back to import_tires function

    fields = ["manufacturer", "category", "tire", "prefix", "treadwidth",
              "profile", "additional_size", "diameter", "ply", "utgq_rating",
              "speed_rating", "load_rating", "sidewall_style", "availability",
              "sku", "quantity", "price", "weight",
              "picture_1", "picture_2", "picture_3", "picture_4",
              "meta_keywords", "meta_description", "description"]

    total_lines = int(sum(1 for line in open(filepath, 'rU')) - 1)

    try:
        freader = csv.reader(open(filepath, "rU"), quoting=csv.QUOTE_ALL)
    except IOError:
        return

    headings = map(lambda title: title.lower().strip(), freader.next())

    if fields != headings:
        import_logger.error("Field headings don't match exactly.")

        # errors.append("Invalid format: The first line must contain\
        #    the following fields in sequence: %s" % ", ".join(fields))

    skudict = {}
    for i, values in enumerate(freader):

        if len(values) != len(fields):
            import_logger.warning("Skipped row because fields do not match with values")
            continue

        row = dict(zip(fields, values))

        # Try to fix data and if it doesn't work, return None
        row, errors = clean(row)
        if errors:
            for error in errors:
                import_logger.error(error)
            continue

        skudict = process(row, skudict)

    '''
        import_tires.update_state(state="WORKING",
            meta={'current': i, 'total': total_lines})

    # Mark task as completed
    task = Task.objects.get(task=import_tires.request.id)
    task.is_completed = True
    task.save()
    '''


# @task
def import_wheels(filepath, model='wheel'):
    def clean(row):
        errors = []
        NULL_FIELDS = ["boltpattern_2", "availability", "quantity",
                       "picture_1", "picture_2", "picture_3", "picture_4",
                       "meta_keywords", "meta_description", "description"]

        # Check if there are any fields that are required but have value missing
        for item in row.keys():
            if row[item]:
                row[item] = str(row[item]).strip()
            else:
                required_but_missing_fields = []

                if item not in NULL_FIELDS:
                    required_but_missing_fields.append(item.title())

                if required_but_missing_fields:
                    error = "Field(s) ({0}) missing in SKU {1}.".format(
                        ",".join(required_but_missing_fields), row['sku'])
                    errors.append(error)

        # Make all fields unicode
        for f in row.keys():
            try:
                row[f] = unicode(row[f], errors='replace')
            except TypeError:
                row[f] = unicode(str(row[f]), errors='replace')

        # Fix Data types
        INTEGER_FIELDS = ['offset', 'diameter', 'quantity', 'availability']
        for field in INTEGER_FIELDS:
            if not row[field]:
                row[field] = '0.0'
            row[field] = int(float(row[field]))

        row['diameter'] = float(row['diameter'])
        row['wheelwidth'] = float(row['wheelwidth'])

        # Fix weight
        if not row['weight']:
            row['weight'] = 40
        else:
            row['weight'] = row['weight']
        row['weight_unit'] = 'lb'

        # Check quantity
        if not row['quantity']:
            row['quantity'] = 0

        # Fix the thumbnail paths
        for i in range(1, 5):
            if row['picture_%s' % i]:
                row['picture_%s' % i] = "media/wheels/" + row['picture_%s' % i]
            else:
                row['picture_%s' % i] = None

        # Check price
        try:
            row['price'] = Decimal(sub(r'[^\d.]', '', row['price']))
        except InvalidOperation:
            errors.append("Invalid value for price ({0}) for SKU ({1})".format(
                row['price'], row['sku']))

        return row, errors

    # @transaction.commit_on_success
    def process(row, errors, skudict):
        # WheelManufacturer
        manufacturers = WheelManufacturer.objects.filter(name=row.get('manufacturer'))
        # num_manufacturers = len(manufacturers)
        num_manufacturers = manufacturers.count()
        if num_manufacturers > 0:
            manufacturer = manufacturers[0]
        else:
            manufacturer = WheelManufacturer(
                name=row.get('manufacturer')
            )
            manufacturer.save()
        row['manufacturer'] = manufacturer

        # Wheel
        wheel, is_created = Wheel.objects.get_or_create(
            manufacturer=row.get('manufacturer'),
            name=row.get('wheel')
        )
        if is_created:
            wheel.meta_keywords = row.get('meta_keywords')
            wheel.meta_description = row.get('meta_description')
            wheel.description = row.get('description')
            wheel.save()
        row['wheel'] = wheel

        # Wheel Picture
        for i in range(1, 5):
            picture = row.get('picture_%s' % i, None)
            if picture:
                wheelpicture, is_created = WheelPicture.objects.get_or_create(
                    wheel=wheel,
                    picture=picture
                )
                wheelpicture.save()

        # Wheel Size
        wheelsize_dict = row.copy()
        del (wheelsize_dict['manufacturer'])

        for i in range(1, 5):
            del (wheelsize_dict['picture_%s' % i])

        del (wheelsize_dict['meta_keywords'])
        del (wheelsize_dict['meta_description'])
        del (wheelsize_dict['description'])

        sku = row.get('sku').strip()
        if skudict.get(sku):
            msg = "Duplicate products with the same sku %s found." % sku
            import_logger.error(msg)
            errors.append(msg)
            return (errors, skudict)
        else:
            skudict[sku] = True
        try:
            wheelsize = WheelSize.objects.get(sku=sku)
        except WheelSize.DoesNotExist:

            wheelsize = WheelSize.objects.create(**wheelsize_dict)
            # if True:
            #  try:
            #    wheelsize.save()
            #  except:
            #    raise Exception(sku)
            '''
            except:
                msg = "Error saving the row with sku %s" % sku
                import_logger.error(msg)
                errors.append(msg)
                '''
        else:
            for field in wheelsize_dict:
                setattr(wheelsize, field, wheelsize_dict.get(field))
            wheelsize.save()

        return (errors, skudict)

    errors = []
    fields = ["manufacturer", "wheel", "finish", "diameter", "wheelwidth",
              "boltpattern_1", "boltpattern_2", "offset", "centerbore",
              "availability", "sku", "quantity", "price", "weight",
              "picture_1", "picture_2", "picture_3", "picture_4",
              "meta_keywords", "meta_description", "description"]

    total_lines = int(sum(1 for line in open(filepath, 'rU')) - 1)

    try:
        freader = csv.reader(open(filepath, "rU"), quoting=csv.QUOTE_ALL)
    except IOError:
        return

    headings = map(lambda title: title.lower().strip(), freader.next())

    import_logger.debug(headings)

    if fields != headings:
        import_logger.error("Field headings don't match exactly.")

    skudict = {}
    for i, values in enumerate(freader):

        if len(values) != len(fields):
            msg = "Skipped row {0} because fields do not match with values".format(i)
            import_logger.warning(msg)
            errors.append(msg)
            continue

        row = dict(zip(fields, values))

        # Try to fix data and if it doesn't work, return None
        row, errors = clean(row)
        if errors:
            for error in errors:
                import_logger.error(error)
                errors.append(msg)
            continue

        (errors, skudict) = process(row, errors, skudict)
    return errors


'''
        import_wheels.update_state(state="WORKING",meta={'current': i, 'total': total_lines})

    # Mark task as completed
    task = Task.objects.get(task=import_wheels.request.id)
    task.is_completed = True
    task.save()
'''

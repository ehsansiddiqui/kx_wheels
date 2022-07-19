import os
import string
import csv
from random import choice
from decimal import Decimal, InvalidOperation

from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.template.loader import render_to_string

from kxwheels.apps.shop.models import BaseProduct


@staff_member_required
def csv_update(request, content_type_id=None):
    """ 
    Handles updating product quantity, price and availability in bulk. Since 
    product is an abstract model, we need content_type_id to work with as param 
    
    NOTE: This function is NOT completely generic because it refers to
    "availability" field of a subclass. Getting rid of all the references to 
    this field will make this function generic again.
    """
    context = {}
    content_type = ContentType.objects.get(pk=int(content_type_id))
    if not issubclass(content_type.model_class(), BaseProduct):
        raise Exception(content_type)

    # Generate a random name for temporary file
    temp_file = ''.join([choice(string.letters + string.digits) for i in range(10)])
    temp_file_path = '/tmp/%s.csv' % temp_file

    # Errors and results holders
    errors, result = [], []

    if request.method == "POST":

        # Read the uploaded file and store it in a temporary file
        uploaded_file = request.FILES.get('file')

        if uploaded_file:
            fsock = open(temp_file_path, 'wb+')
            for chunk in uploaded_file.chunks():
                fsock.write(chunk)
            fsock.close()

        # Try opening the temporary file and validate the header line
        try:
            freader = csv.reader(open(temp_file_path), delimiter=',', quotechar='"')
        except IOError:
            errors.append("No file was uploaded.")
        else:
            header = freader.next()
            if (header[0].lower() != "sku" or header[1].lower() != "quantity" or
                        header[2].lower() != "price" or header[3].lower() != "availability"):
                errors.append("Invalid format: The first line must contain\
                    the following fields: sku, quantity, price, availability")

        if not errors:
            for row in freader:
                # Skip empty lines
                if len(row) < 1:
                    continue

                try:
                    sku = row[0].strip()
                except IndexError:
                    sku = None

                try:
                    quantity = int(row[1].strip())
                except (IndexError, ValueError):
                    quantity = None

                try:
                    price = Decimal(row[2].strip())
                except (IndexError, ValueError, InvalidOperation):
                    price = None

                try:
                    availability = int(row[3].strip())
                except (IndexError, ValueError):
                    availability = None

                if None in [sku, quantity, price, availability]:
                    errors.append("(%s, %s, %s, %s) - Invalid row (skipped)." %
                                  (sku, quantity, price, availability))
                else:
                    try:
                        object = content_type.get_object_for_this_type(sku=sku)
                    except:
                        errors.append("(%s, %s, %s, %s) - New row (skipped)." %
                                      (sku, quantity, price, availability))
                        continue
                    else:
                        object.quantity = quantity
                        object.price = price
                        object.availability = availability
                        object.save()
                        result.append("(%s - %s - %s - %s) updated." %
                                      (sku, quantity, price, availability))
            os.remove(temp_file_path)

    context['errors'] = errors
    context['result'] = result

    return HttpResponse(render_to_string(request=request,
                                         template_name="admin/shop/product/csv_import.html",
                                         context=context))

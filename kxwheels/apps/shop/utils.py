import os
import re
import unicodedata
import random
import string
#import ho.pisa as pisa
import cStringIO as StringIO
from django.conf import settings
from django.template import Context
from django.http import HttpResponse
from htmlentitydefs import name2codepoint
from django.template.loader import get_template
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import smart_unicode, force_unicode

# http://djangosnippets.org/snippets/814/
def byte_to_base32_chr(byte):
    # alphabet will become our base-32 character set:
    alphabet = string.uppercase + string.digits 
    # We must remove 4 characters from alphabet to make it 32 characters long. We want it to be 32
    # characters long so that we can use a whole number of random bits to index into it.
    for loser in 'l1o0': # Choose to remove ones that might be visually confusing
        i = alphabet.index(loser)
        alphabet = alphabet[:i] + alphabet[i+1:]
    return alphabet[byte & 31]

def random_id(length):
    # Can easily be converted to use secure random when available
    # see http://www.secureprogramming.com/?action=view&feature=recipes&recipeid=20
    random_bytes = [random.randint(0, 0xFF) for i in range(length)]
    return ''.join(map(byte_to_base32_chr, random_bytes))


# Borrowed from http://bitbucket.org/breadandpepper/django-brookie/
    
def fetch_resources(uri, rel):
    """
    Callback to allow pisa/reportlab to retrieve Images,Stylesheets, etc.
    `uri` is the href attribute from the html link element.
    `rel` gives a relative path, but it's not used here.
    """
    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    return path

def generate_pdf(filename, context_dict, template):
    
    template = get_template(template)
    context = Context(context_dict)
    html  = template.render(context)
    # Insert page skips
    html = html.replace('-pageskip-', '<pdf:nextpage />')
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(
        html.encode("UTF-8")), result, link_callback=fetch_resources)
    if pdf.err:
        return HttpResponse('Error creating your PDF: %s' % cgi.escape(html))
    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=%s.pdf' % filename
    return response

def slugify(s, entities=True, decimal=True, hexadecimal=True,
   instance=None, slug_field='slug', filter_dict=None):
    s = smart_unicode(s)

    #character entity reference
    if entities:
        s = re.sub('&(%s);' % '|'.join(name2codepoint), lambda m: unichr(name2codepoint[m.group(1)]), s)

    #decimal character reference
    if decimal:
        try:
            s = re.sub('&#(\d+);', lambda m: unichr(int(m.group(1))), s)
        except:
            pass

    #hexadecimal character reference
    if hexadecimal:
        try:
            s = re.sub('&#x([\da-fA-F]+);', lambda m: unichr(int(m.group(1), 16)), s)
        except:
            pass

    #translate
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')

    #replace unwanted characters
    s = re.sub(r'[^-a-z0-9]+', '-', s.lower())

    #remove redundant -
    s = re.sub('-{2,}', '-', s).strip('-')

    slug = s
    if instance:
        def get_query():
            query = instance.__class__.objects.filter(**{slug_field: slug})
            if filter_dict:
                query = query.filter(**filter_dict)
            if instance.pk:
                query = query.exclude(pk=instance.pk)
            return query
        counter = 1
        while get_query():
            slug = "%s-%s" % (s, counter)
            counter += 1
    return slug

def is_valid_generic_object(content_type_id, object_id):
    """docstring for validate_generic_object"""
    # Validate content_type
    try:
        content_type=ContentType.objects.get(pk=content_type_id)
    except ContentType.DoesNotExist:
        return False

    # Validate object
    try:
        valid_obj=content_type.get_object_for_this_type(pk=object_id)
    except ObjectDoesNotExist:
        return False
        
    return True

def is_valid_cc(s):
    """
    http://atlee.ca/blog/2008/05/27/validating-credit-card-numbers-in-python/
    
    Returns True if the credit card number ``s`` is valid,
    False otherwise.

    Returning True doesn't imply that a card with this number has ever been,
    or ever will be issued.

    Currently supports Visa, Mastercard, American Express, Discovery
    and Diners Cards.  

    >>> validate_cc("4111-1111-1111-1111")
    True
    >>> validate_cc("4111 1111 1111 1112")
    False
    >>> validate_cc("5105105105105100")
    True
    >>> validate_cc(5105105105105100)
    True
    """
    # Strip out any non-digits
    # Jeff Lait for Prime Minister!
    s = re.sub("[^0-9]", "", str(s))
    regexps = [
            "^4\d{15}$",
            "^5[1-5]\d{14}$",
            "^3[4,7]\d{13}$",
            "^3[0,6,8]\d{12}$",
            "^6011\d{12}$",
            ]

    if not any(re.match(r, s) for r in regexps):
        return False

    chksum = 0
    x = len(s) % 2

    for i, c in enumerate(s):
        j = int(c)
        if i % 2 == x:
            k = j*2
            if k >= 10:
                k -= 9
            chksum += k
        else:
            chksum += j

    return chksum % 10 == 0

def handle_file_upload(model, tmp_file_path, file):


    from django.core.management import call_command
    
    rel = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)
    
    _path = '../../tmp'
    if not os.path.exists(rel(_path)):
        os.makedirs(rel(_path))
        
    _path = '../../tmp/dbdumps/%s' % model
    if not os.path.exists(rel(_path)):
        os.makedirs(rel(_path))
    dbdump_path = rel(_path)
    
    # Create a backup
    sys.stdout = open('%s/%s.json' % (dbdump_path, str(int(time.time()))), 'w')
    call_command('dumpdata', model, format='json', stdout=sys.stdout)
    sys.stdout.close()
    
    # Read the uploaded file and store it in a temporary file
    if file:
        destination = open(tmp_file_path, 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
    return True

import re
import unicodedata
from uuid import uuid4
from htmlentitydefs import name2codepoint
from django.utils.encoding import smart_unicode, force_unicode
from kxwheels.apps.account.models import Profile


def cut_decimals(input):
    """
    input: floating number
    output: number as string with zero decimals removed
    """
    # print float-int(float)
    # print '%.4f' %float
    if float(input) - int(float(input)) != 0:
        number = '%.4f' % input
        number = number.replace('0.', 'X.')
        number = number.replace('0', '')
        number = number.replace('X.', '0.')
    else:
        number = '%.0f' % float(input)
    return unicode(number)


def slugify(s, entities=True, decimal=True, hexadecimal=True,
            instance=None, slug_field='slug', filter_dict=None):
    s = smart_unicode(s)

    # character entity reference
    if entities:
        s = re.sub('&(%s);' % '|'.join(name2codepoint), lambda m: unichr(name2codepoint[m.group(1)]), s)

    # decimal character reference
    if decimal:
        try:
            s = re.sub('&#(\d+);', lambda m: unichr(int(m.group(1))), s)
        except:
            pass

    # hexadecimal character reference
    if hexadecimal:
        try:
            s = re.sub('&#x([\da-fA-F]+);', lambda m: unichr(int(m.group(1), 16)), s)
        except:
            pass

    # translate
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')

    # replace unwanted characters
    s = re.sub(r'[^-a-z0-9]+', '-', s.lower())

    # remove redundant -
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


def slugify_uuid(s, entities=True, decimal=True, hexadecimal=True):
    s = smart_unicode(s)
    if entities:
        s = re.sub('&(%s);' % '|'.join(name2codepoint), lambda m: unichr(name2codepoint[m.group(1)]), s)

    if decimal:
        try:
            s = re.sub('&#(\d+);', lambda m: unichr(int(m.group(1))), s)
        except:
            pass

    if hexadecimal:
        try:
            s = re.sub('&#x([\da-fA-F]+);', lambda m: unichr(int(m.group(1), 16)), s)
        except:
            pass

    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')
    s = re.sub(r'[^-a-z0-9]+', '-', s.lower())
    s = re.sub('-{2,}', '-', s).strip('-')

    slug = "%s-%s" % (s, uuid4().hex[-5:])
    return slug


def extract_subdomain(request):
    subdomain = None
    subdomain_profile = None
    host = request.META.get('HTTP_HOST', '')
    host_s = host.replace('www.', '').split('.')
    if len(host_s) > 2:
        subdomain = ''.join(host_s[:-2])
        try:
            subdomain_profile = Profile.objects.get(subdomain=subdomain)
        except:
            pass
    return subdomain, subdomain_profile

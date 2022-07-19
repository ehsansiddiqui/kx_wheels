# -*- mode: python; coding: utf-8; -*-
# Borrowed from http://byteflow.su/browser/apps/blog/management/__init__.py
import re
import sys

from django.contrib.sites import models as site_app
from django.contrib.sites.models import Site
from django.db.models import signals
from kxwheels.apps.shop.models import Setting
from kxwheels.apps.l10n.models import (Country, AdminArea)

RE_VALID_DOMAIN = re.compile(r'([A-Z0-9]([A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}')
RE_VALID_EMAIL = re.compile(r'^([^@\s]+)@((?:[-a-z0-9]+\.)+[a-z]{2,})$')
RE_VALID_POSTALCODE = re.compile(r'([A-Z]{1}[0-9]{1}){3}')

def create_site_setting_interactively(app, created_models, verbosity, **kwargs):
    domain, name, store_name, store_email, orders_email, address, city,\
    postal_code, phone, fax = (None,)*10
    
    # Create country
    country, created = Country.objects.get_or_create(
        iso_3166_1='CA', 
        name='Canada', 
        formal_name='Canada',
        continent='NA',
        admin_area='pr',
        postal_type='postal_code',
    )
    
    if created:
        country.save()

    # Create province
    province, created = AdminArea.objects.get_or_create(
        iso_3166_1=country,
        iso_3166_2='BC',
        name='British Columbia',
    )
    
    if created:
        province.save
    
    if set([Site, Setting]) <= created_models:
        if kwargs.get('interactive', True):
            
            msg = "\nYou have just initialized your sites subsystem, which " \
                "means you don't have any \nsites or configurations defined. "\
                "\nWould you like create one now? "
            is_continue = raw_input("%s [yes/no]: " % msg)
            if is_continue in ['n', 'no', 'No', 'NO',]:
                return False

            domain, name, store_name, store_email, orders_email, address, city,\
            postal_code, phone, fax = get_site_setting_interactive()
            try:
                site = Site.objects.all()[0]
                site.domain = domain
                site.name = name
                site.save()
            except IndexError:
                site = None
        if not Site.objects.count():
            Site.objects.create(domain=domain, name=name)

        if site is not None:
            try:
                site_setting = Setting.objects.create(
                    site=site,
                    store_name=store_name,
                    store_email=store_email,
                    store_orders_email=orders_email,
                    street1=address,
                    city=city,
                    province=province,
                    postal_code=postal_code,
                    phone=phone,
                    fax=fax,
                )
                site_setting.save()
            except Exception, e:
                sys.stderr.write("Error: %s\n" % e)
                pass
    Site.objects.clear_cache()

def get_site_setting_interactive():
    domain, name, store_name, store_email, orders_email, address, city,\
    postal_code, phone, fax = [None]*10
    
    while not domain:
        input_msg = 'Domain'
        domain = raw_input(input_msg + ': ')
        if not RE_VALID_DOMAIN.match(domain.upper()):
            sys.stderr.write("Error: domain is invalid\n")
            domain = None

    while not name:
        input_msg = 'Name'
        name = raw_input(input_msg + ': ')
            
    while not store_name:
        input_msg = 'Store name'
        if name:
            input_msg += ' (%r)' % name
        store_name = raw_input(input_msg + ": ")
        if name and not store_name:
            store_name = name
    
    while not store_email:
        input_msg = 'Store email (info@%s)' % domain
        store_email = raw_input(input_msg + ': ')
        if not store_email:
            store_email = str("info@%s" % domain)
        if not RE_VALID_EMAIL.match(store_email):
            sys.stderr.write("Error: store email is invalid\n")
            store_email = None
            
    while not orders_email:
        input_msg = 'Orders email (orders@%s)' % domain
        orders_email = raw_input(input_msg + ': ')
        if not orders_email:
            orders_email = "orders@%s" % domain
        if not RE_VALID_EMAIL.match(orders_email):
            sys.stderr.write("Error: orders email is invalid\n")
            orders_email = None

    while not address:
        input_msg = 'Address'
        address = raw_input(input_msg + ': ')
        
    while not city:
        input_msg = 'City'
        city = raw_input(input_msg + ': ')

    while not postal_code:
        input_msg = 'Postal code'
        postal_code = raw_input(input_msg + ': ').upper()
        if not RE_VALID_POSTALCODE.match(postal_code):
            sys.stderr.write("Error: postal code is invalid\n")
            postal_code = None

    while not phone:
        input_msg = 'Phone'
        phone = raw_input(input_msg + ': ')
        if not unicode(phone).isnumeric() or len(phone) > 10:
            sys.stderr.write("Error: phone number must be 10 digits\n")
            phone = None
            
    while not fax:
        input_msg = 'Fax'
        fax = raw_input(input_msg + ': ')
        if not unicode(fax).isnumeric() or len(fax) > 10:
            sys.stderr.write("Error: fax number must be 10 digits\n")
            fax = None

    return domain, name, store_name, store_email, orders_email, address, city,\
            postal_code, phone, fax

signals.post_syncdb.connect(create_site_setting_interactively, sender=site_app)
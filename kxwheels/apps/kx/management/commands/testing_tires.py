import re
import requests
import json
import ast
import random
import traceback
import StringIO
import xlsxwriter

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage

from pandas import DataFrame
from xlsxwriter.workbook import Workbook
from pyquery import PyQuery
from datetime import datetime
from time import sleep
import kxwheels.settings.base as settings
from django.core.management.base import BaseCommand
from kxwheels.apps.kx.models.wheel import *
from kxwheels.apps.vehicle.models import *
from kxwheels.apps.kx.models.wheel import *
from kxwheels.apps.kx.models.tire import *


class Command(BaseCommand):

    # def add_arguments(self, parser):
    #     parser.add_argument('brand_name',
    #         help='Fulfill orders updated before threshold (seconds)')

    def handle(self, *args, **options):
        missing_brand_model = []
        missing_brand_model1 = []
        missing_brand = []
        missing_brand1 = []
        missing_year = []
        missing_year1 = []
        years_list = []
        year_value = 1965
        while year_value <= 2018 :
            years_list.append(year_value)
            year_value = year_value + 1

        brands = Manufacturer.objects.all()
        for brand in brands:
            for years in years_list:
                model_in_year = Model.objects.filter(manufacturer=brand.id, year=years)
                if model_in_year:
                    pass
                else:
                    pass
                for model_year in model_in_year:
                    tire_size_st = model_year.get_oe_staggered_tire_sizes()
                    tire_size = model_year.get_oe_tire_sizes()
                    if not tire_size_st and not tire_size:
                        missing_brand_model.append(model_year.name)
                        missing_brand.append(brand)
                        missing_year.append(years)
                    else:
                        pass

        workbook = xlsxwriter.Workbook('search_list_tires.xlsx')
        worksheet = workbook.add_worksheet()

        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:B', 20)
        worksheet.set_column('C:C', 20)
        worksheet.set_column('D:D', 20)
        worksheet.set_column('E:E', 20)
        bold = workbook.add_format({'bold': True})
        worksheet.write('A1', 'List of Brands, Year and Model for which Tires are Missing.', bold)
        worksheet.write('B3', 'Missing Tire Brand', bold)
        worksheet.write('C3', 'Missing Tire year',bold)
        worksheet.write('D3', 'Missing Tire Model', bold)

        i = 0
        while i < len(missing_brand):
            row = i +4
            worksheet.write( row, 1,str(missing_brand[i]))
            worksheet.write( row, 2, str(missing_year[i]))
            worksheet.write( row, 3, str(missing_brand_model[i]))
            i += 1

        workbook.close()

        mail = EmailMessage('Kxwheels Scrapper Email', 'List of Missing Models and Wheels in Quic Search.', settings.DEFAULT_FROM_EMAIL, to=['zaheer.asp2@gmail.com'])
        mail.attach_file( '/var/www/html/kxwheels/search_list_tires.xlsx', 'text/csv')
        mail.send()



    def get_resource(self, target_url, cookies=''):

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }

        headers['Cookie'] = '__qca=P0-1966566132-1506078970718; _ga=GA1.2.1655158944.1506078970; _gid=GA1.2.1259786425.1506321219; sessionid=fw1sg0wjdpdixi1dzjbt4no5uhuzcrok; csrftoken=Wcqfpxl1Lkn6wKwpftyWIsYf38TkrCgr; _gali=id_make'
        return requests.get(target_url, headers=headers)

    def print_message(self, message=''):
        self.stdout.write(message)

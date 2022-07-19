import re
import requests
import json
import ast
import random
import traceback

from pyquery import PyQuery
from datetime import datetime
from time import sleep
import kxwheels.settings.base as settings
from django.core.management.base import BaseCommand
from kxwheels.apps.kx.models.wheel import *

class Command(BaseCommand):

    site_url = "http://www.mhtwheels.com"
    url = "http://www.mhtwheels.com/fuel-b-627.htm"
    cookies = "cfid=1410095b-b023-44a5-ab8f-07092072664d; cftoken=0; JSESSIONID=43ADB2A50B4C89B3D68E4D021C9EBE27; AWSELB=43AF81CF1EB49B01AF2671E8C2F02F88D67DD1E05C3FEA1FF0D02634C60074D9271777735049AD08A45C1CF35D82FEBCF3544A7C98E3802CC33316B50A6B180CCFA790BD16; _ga=GA1.2.1046488419.1495710091; _gid=GA1.2.1581180477.1495783273; _gat=1"

    def add_arguments(self, parser):
        parser.add_argument('brand_name',
            help='Fulfill orders updated before threshold (seconds)')

    def handle(self, *args, **options):
        page = self.get_resource(self.url, self.cookies)
        if page.status_code == 200:
            content = page.text
            pq = PyQuery(content)
            self.print_message("Scrapping wheels")
            for items in pq('div.wheels-list').items():
                product_url = self.site_url + items('a').attr['href']
                image = items('img').attr['src']
                inner_page = self.get_resource(product_url, self.cookies)
                if inner_page.status_code == 200:
                    inner_page_content = inner_page.text
                    pq1 = PyQuery(inner_page_content)
                    if pq1('div.row').attr['id'] == "wheel" and pq1('div.specs'):
                        for row in pq1('table tbody tr').items():
                            text = row('td').text()
                            for sku in text.split(' '):
                                if len(sku) == 12:
                                    try:
                                        wheel = WheelScrappedPictures.objects.get(part_no=sku)
                                        self.print_message("Already exist skipping this")
                                    except WheelScrappedPictures.DoesNotExist:
                                        wheel = WheelScrappedPictures(
                                            part_no=sku,
                                            pic_url=image
                                        )
                                        wheel.save()
                                        self.print_message("Image saved")

                sleep(0.5)

    def get_resource(self, target_url, cookies=''):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }

        if cookies:
            headers['Cookie'] = cookies
        return requests.get(target_url, headers=headers)

    def print_message(self, message=''):
        self.stdout.write(message)

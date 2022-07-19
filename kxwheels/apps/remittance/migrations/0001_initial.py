# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=255, verbose_name='email')),
                ('billing_first_name', models.CharField(max_length=255, verbose_name='billing first name')),
                ('billing_last_name', models.CharField(max_length=255, verbose_name='billing last name')),
                ('billing_company_name', models.CharField(max_length=255, verbose_name='billing company name')),
                ('billing_address_1', models.CharField(max_length=255, verbose_name='billing address line 1')),
                ('billing_address_2', models.CharField(max_length=255, verbose_name='billing address line 2')),
                ('billing_city', models.CharField(max_length=255, verbose_name='billing city')),
                ('billing_province', models.CharField(max_length=255, verbose_name='billing province')),
                ('billing_postal_code', models.CharField(max_length=255, verbose_name='billing postal code')),
                ('billing_country', models.CharField(max_length=255, verbose_name='billing country')),
                ('billing_email', models.EmailField(max_length=255, verbose_name='billing email')),
                ('billing_phone', models.CharField(max_length=255, verbose_name='billing phone')),
                ('billing_fax', models.CharField(max_length=255, verbose_name='billing fax')),
                ('is_shipping_same_billing', models.BooleanField(default=True, verbose_name='is_shipping_same_billing')),
                ('shipping_first_name', models.CharField(max_length=255, verbose_name='shipping first name')),
                ('shipping_last_name', models.CharField(max_length=255, verbose_name='shipping last name')),
                ('shipping_company_name', models.CharField(max_length=255, verbose_name='shipping company name')),
                ('shipping_address_1', models.CharField(max_length=255, verbose_name='shipping address line 1')),
                ('shipping_address_2', models.CharField(max_length=255, verbose_name='shipping address line 2')),
                ('shipping_city', models.CharField(max_length=255, verbose_name='shipping city')),
                ('shipping_province', models.CharField(max_length=255, verbose_name='shipping province')),
                ('shipping_postal_code', models.CharField(max_length=255, verbose_name='shipping postal code')),
                ('shipping_country', models.CharField(max_length=255, verbose_name='shipping country')),
                ('shipping_email', models.EmailField(max_length=255, verbose_name='shipping email')),
                ('shipping_phone', models.CharField(max_length=255, verbose_name='shipping phone')),
                ('shipping_fax', models.CharField(max_length=255, verbose_name='shipping fax')),
                ('customer', models.ForeignKey(verbose_name='customer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'buyer',
                'verbose_name_plural': 'buyers',
            },
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.CharField(unique=True, max_length=32, blank=True)),
                ('order', models.CharField(max_length=255, verbose_name='order number')),
                ('subtotal', models.DecimalField(null=True, verbose_name='subtotal', max_digits=16, decimal_places=2, blank=True)),
                ('tax', models.DecimalField(null=True, verbose_name='tax', max_digits=16, decimal_places=2, blank=True)),
                ('shipping', models.DecimalField(null=True, verbose_name='shipping & handling', max_digits=16, decimal_places=2, blank=True)),
                ('discount', models.DecimalField(null=True, verbose_name='discount', max_digits=16, decimal_places=2, blank=True)),
                ('total', models.DecimalField(null=True, verbose_name='total', max_digits=16, decimal_places=2, blank=True)),
                ('currency', models.CharField(max_length=3, verbose_name='ISO currency code')),
                ('note', models.TextField(null=True, verbose_name='purchase note', blank=True)),
                ('buyer', models.ForeignKey(related_name='purchases', verbose_name='buyer', to='remittance.Buyer')),
            ],
            options={
                'verbose_name': 'purchase',
                'verbose_name_plural': 'purchases',
            },
        ),
        migrations.CreateModel(
            name='PurchaseItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sku', models.CharField(max_length=255, verbose_name='sku')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('desc', models.TextField(max_length=255, null=True, verbose_name='desc')),
                ('qty', models.IntegerField(verbose_name='qty')),
                ('unit_price', models.DecimalField(null=True, verbose_name='unit price', max_digits=16, decimal_places=2, blank=True)),
                ('discount', models.DecimalField(decimal_places=2, default=b'-0.00', max_digits=16, blank=True, null=True, verbose_name='discount')),
                ('ext_price', models.DecimalField(null=True, verbose_name='extended price', max_digits=16, decimal_places=2, blank=True)),
                ('tax', models.DecimalField(null=True, verbose_name='tax', max_digits=16, decimal_places=2, blank=True)),
                ('purchase', models.ForeignKey(related_name='items', verbose_name='purchase', to='remittance.Purchase')),
            ],
            options={
                'verbose_name': 'purchase item',
                'verbose_name_plural': 'purchase items',
            },
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=255, verbose_name='first name')),
                ('last_name', models.CharField(max_length=255, verbose_name='last name')),
                ('company_name', models.CharField(max_length=255, verbose_name='company name')),
                ('address_1', models.CharField(max_length=255, verbose_name='address line 1')),
                ('address_2', models.CharField(max_length=255, null=True, verbose_name='address line 2')),
                ('city', models.CharField(max_length=255, verbose_name='city')),
                ('province', models.CharField(max_length=255, verbose_name='province')),
                ('postal_code', models.CharField(max_length=255, verbose_name='postal code')),
                ('country', models.CharField(max_length=255, verbose_name='country')),
                ('email', models.EmailField(max_length=255, verbose_name='email')),
                ('phone', models.CharField(max_length=255, verbose_name='phone')),
                ('fax', models.CharField(max_length=255, verbose_name='fax')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('trans_id', models.CharField(max_length=45, serialize=False, verbose_name='Transaction ID', primary_key=True)),
                ('trans_type', models.CharField(max_length=45, verbose_name='Transaction Type')),
                ('trans_datetime', models.DateTimeField(verbose_name='Transaction Datetime')),
                ('amount', models.DecimalField(default=b'0.00', verbose_name='Amount', max_digits=18, decimal_places=4)),
                ('method', models.CharField(max_length=255, verbose_name='Method')),
                ('gateway', models.CharField(max_length=255, verbose_name='Gateway')),
                ('auth_code', models.CharField(max_length=255, verbose_name='Auth Code')),
                ('iso_code', models.CharField(max_length=255, verbose_name='ISO Code')),
                ('response_code', models.CharField(max_length=255, verbose_name='Response Code')),
                ('reason_code', models.CharField(max_length=255, verbose_name='Reason Code')),
                ('message', models.CharField(max_length=255, verbose_name='Message')),
                ('is_success', models.BooleanField(default=False, verbose_name='Approved?')),
                ('raw', models.TextField(verbose_name='Raw')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('paypal_email', models.CharField(max_length=255, null=True, verbose_name='paypal_email', blank=True)),
                ('purchase', models.ForeignKey(related_name='transactions', verbose_name='Purchase', to='remittance.Purchase')),
            ],
            options={
                'verbose_name': 'transaction',
                'verbose_name_plural': 'transactions',
            },
        ),
        migrations.AddField(
            model_name='purchase',
            name='seller',
            field=models.ForeignKey(related_name='purchases', verbose_name='seller', to='remittance.Seller'),
        ),
    ]

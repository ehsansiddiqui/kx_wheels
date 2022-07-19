# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('sites', '0001_initial'),
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BoltPattern',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(unique=True, max_length=10, verbose_name=b'Value')),
                ('sort_order', models.IntegerField(null=True, verbose_name=b'Sort order', blank=True)),
            ],
            options={
                'ordering': ('id',),
                'verbose_name': 'bolt pattern',
                'verbose_name_plural': 'bolt patterns',
            },
        ),
        migrations.CreateModel(
            name='Diameter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(unique=True, max_length=6, verbose_name='value')),
                ('ordering', models.IntegerField(null=True, verbose_name='sort order', blank=True)),
            ],
            options={
                'verbose_name': 'diameter',
                'verbose_name_plural': 'diameters',
            },
        ),
        migrations.CreateModel(
            name='Finish',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(unique=True, max_length=50, verbose_name=b'Value')),
                ('sort_order', models.IntegerField(null=True, verbose_name=b'Sort order', blank=True)),
            ],
            options={
                'ordering': ('value',),
                'verbose_name': 'finish',
                'verbose_name_plural': 'finishes',
            },
        ),
        migrations.CreateModel(
            name='FrontWheelSize',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('diameter_range', models.CharField(max_length=50, null=True, verbose_name='diameter range', blank=True)),
                ('wheelwidth_range', models.CharField(max_length=50, null=True, verbose_name='wheel width range', blank=True)),
                ('offset_range', models.CharField(max_length=50, null=True, verbose_name='offset range', blank=True)),
            ],
            options={
                'verbose_name': 'Front Wheel Size',
                'verbose_name_plural': 'Front Wheel Sizes',
            },
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='slug', blank=True)),
                ('picture', sorl.thumbnail.fields.ImageField(upload_to=b'pictures/vehicles/manufacturer', null=True, verbose_name='picture', blank=True)),
                ('ordering', models.IntegerField(null=True, verbose_name='sort order', blank=True)),
                ('is_active', models.BooleanField(default=1)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'manufacturer',
                'verbose_name_plural': 'manufacturers',
            },
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='model')),
                ('year', models.IntegerField(verbose_name='year')),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='slug', blank=True)),
                ('boltpattern', models.CharField(max_length=50, verbose_name='bolt pattern', blank=True)),
                ('centerbore', models.CharField(max_length=6, null=True, verbose_name='centerbore', blank=True)),
                ('ordering', models.IntegerField(null=True, verbose_name='sort order', blank=True)),
                ('is_active', models.BooleanField(default=1)),
                ('manufacturer', models.ForeignKey(related_name='models', verbose_name='manufacturer', to='vehicle.Manufacturer')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'model',
                'verbose_name_plural': 'models',
            },
        ),
        migrations.CreateModel(
            name='OEStaggeredTireSize',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('front_prefix', models.CharField(default=b'', max_length=5, null=True, blank=True)),
                ('front_treadwidth', models.CharField(max_length=6)),
                ('front_profile', models.CharField(max_length=6)),
                ('front_additional_size', models.CharField(default=b'', max_length=5, null=True, blank=True)),
                ('front_diameter', models.CharField(max_length=6)),
                ('rear_prefix', models.CharField(default=b'', max_length=5, null=True, blank=True)),
                ('rear_treadwidth', models.CharField(max_length=6)),
                ('rear_profile', models.CharField(max_length=6)),
                ('rear_additional_size', models.CharField(default=b'', max_length=5, null=True, blank=True)),
                ('rear_diameter', models.CharField(max_length=6)),
                ('model', models.ForeignKey(related_name='oe_staggered_tire_sizes', to='vehicle.Model')),
            ],
            options={
                'verbose_name': 'OE Staggered Tire Size',
                'verbose_name_plural': 'OE Staggered Tire Sizes',
            },
        ),
        migrations.CreateModel(
            name='OETireSize',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('prefix', models.CharField(default=b'', max_length=5, null=True, blank=True)),
                ('treadwidth', models.CharField(max_length=6)),
                ('profile', models.CharField(max_length=6)),
                ('additional_size', models.CharField(default=b'', max_length=5, null=True, blank=True)),
                ('diameter', models.CharField(max_length=6)),
                ('model', models.ForeignKey(related_name='oe_tire_sizes', to='vehicle.Model')),
            ],
            options={
                'verbose_name': 'OE Tire Size',
                'verbose_name_plural': 'OE Tire Sizes',
            },
        ),
        migrations.CreateModel(
            name='PlusStaggeredTireSize',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('front_prefix', models.CharField(default=b'', max_length=5, null=True, blank=True)),
                ('front_treadwidth', models.CharField(max_length=6)),
                ('front_profile', models.CharField(max_length=6)),
                ('front_additional_size', models.CharField(default=b'', max_length=5, null=True, blank=True)),
                ('front_diameter', models.CharField(max_length=6)),
                ('rear_prefix', models.CharField(default=b'', max_length=5, null=True, blank=True)),
                ('rear_treadwidth', models.CharField(max_length=6)),
                ('rear_profile', models.CharField(max_length=6)),
                ('rear_additional_size', models.CharField(default=b'', max_length=5, null=True, blank=True)),
                ('rear_diameter', models.CharField(max_length=6)),
                ('model', models.ForeignKey(related_name='plus_staggered_tire_sizes', to='vehicle.Model')),
            ],
            options={
                'verbose_name': 'Plus Staggered Tire Size',
                'verbose_name_plural': 'Plus Staggered Tire Sizes',
            },
        ),
        migrations.CreateModel(
            name='PlusTireSize',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('prefix', models.CharField(default=b'', max_length=5, null=True, blank=True)),
                ('treadwidth', models.CharField(max_length=6)),
                ('profile', models.CharField(max_length=6)),
                ('additional_size', models.CharField(default=b'', max_length=5, null=True, blank=True)),
                ('diameter', models.CharField(max_length=6)),
                ('model', models.ForeignKey(related_name='plus_tire_sizes', to='vehicle.Model')),
            ],
            options={
                'verbose_name': 'Plus Tire Size',
                'verbose_name_plural': 'Plus Tire Sizes',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(unique=True, max_length=6, verbose_name='value')),
                ('ordering', models.IntegerField(null=True, verbose_name='sort order', blank=True)),
            ],
            options={
                'verbose_name': 'profile',
                'verbose_name_plural': 'profiles',
            },
        ),
        migrations.CreateModel(
            name='RearWheelSize',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('diameter_range', models.CharField(max_length=50, null=True, verbose_name='diameter range', blank=True)),
                ('wheelwidth_range', models.CharField(max_length=50, null=True, verbose_name='wheel width range', blank=True)),
                ('offset_range', models.CharField(max_length=50, null=True, verbose_name='offset range', blank=True)),
                ('model', models.OneToOneField(related_name='rear_wheel_size', to='vehicle.Model')),
            ],
            options={
                'verbose_name': 'Rear Wheel Size',
                'verbose_name_plural': 'Rear Wheel Sizes',
            },
        ),
        migrations.CreateModel(
            name='TPMS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sku', models.CharField(max_length=255, unique=True, null=True, verbose_name='SKU', blank=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('slug', models.SlugField(help_text='Leave blank to auto-generate', max_length=255, verbose_name='slug', blank=True)),
                ('short_desc', models.CharField(max_length=255, null=True, verbose_name='short description', blank=True)),
                ('long_desc', models.TextField(null=True, verbose_name='long description', blank=True)),
                ('quantity', models.IntegerField(default=1, help_text='in stock', verbose_name='quantity')),
                ('cost', models.DecimalField(null=True, verbose_name='cost', max_digits=16, decimal_places=4, blank=True)),
                ('price', models.DecimalField(verbose_name='price', max_digits=16, decimal_places=4)),
                ('special_price', models.DecimalField(null=True, verbose_name='special price', max_digits=16, decimal_places=4, blank=True)),
                ('spvf', models.DateTimeField(null=True, verbose_name='special price valid from', blank=True)),
                ('spvt', models.DateTimeField(null=True, verbose_name='special price valid till', blank=True)),
                ('meta_title', models.CharField(max_length=255, null=True, verbose_name='meta title', blank=True)),
                ('meta_keywords', models.CharField(max_length=255, null=True, verbose_name='meta keywords', blank=True)),
                ('meta_description', models.CharField(max_length=500, null=True, verbose_name='meta description', blank=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='is active?')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('weight', models.DecimalField(null=True, verbose_name='weight', max_digits=8, decimal_places=2, blank=True)),
                ('weight_unit', models.CharField(default=b'kg', max_length=b'50', verbose_name='weight unit')),
                ('length', models.DecimalField(null=True, verbose_name='length', max_digits=8, decimal_places=2, blank=True)),
                ('length_unit', models.CharField(default=b'm', max_length=b'50', verbose_name='length unit')),
                ('width', models.DecimalField(null=True, verbose_name='width', max_digits=8, decimal_places=2, blank=True)),
                ('width_unit', models.CharField(default=b'm', max_length=b'50', verbose_name='width unit')),
                ('height', models.DecimalField(null=True, verbose_name='height', max_digits=8, decimal_places=2, blank=True)),
                ('height_unit', models.CharField(default=b'm', max_length=b'50', verbose_name='height unit')),
                ('sensor', models.CharField(max_length=200, verbose_name='sensor')),
                ('options', models.ManyToManyField(to='shop.Option', verbose_name='Options', blank=True)),
                ('real_type', models.ForeignKey(editable=False, to='contenttypes.ContentType', null=True)),
                ('site', models.ForeignKey(verbose_name='site', blank=True, to='sites.Site')),
                ('tax', models.ManyToManyField(to='shop.TaxClass', verbose_name='tax', blank=True)),
                ('vehicle', models.OneToOneField(related_name='tpms', verbose_name='vehicle', to='vehicle.Model')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TreadWidth',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(unique=True, max_length=6, verbose_name='value')),
                ('ordering', models.IntegerField(null=True, verbose_name='sort order', blank=True)),
            ],
            options={
                'verbose_name': 'treadwidth',
                'verbose_name_plural': 'treadwidths',
            },
        ),
        migrations.CreateModel(
            name='WheelWidth',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(unique=True, max_length=6, verbose_name=b'Value')),
                ('sort_order', models.IntegerField(null=True, verbose_name=b'Sort order', blank=True)),
            ],
            options={
                'verbose_name': 'wheel width',
                'verbose_name_plural': 'wheel widths',
            },
        ),
        migrations.AddField(
            model_name='frontwheelsize',
            name='model',
            field=models.OneToOneField(related_name='front_wheel_size', to='vehicle.Model'),
        ),
        migrations.AlterUniqueTogether(
            name='model',
            unique_together=set([('manufacturer', 'name', 'year')]),
        ),
    ]

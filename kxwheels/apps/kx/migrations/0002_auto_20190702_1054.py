# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('kx', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sites', '0001_initial'),
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wheelsize',
            name='options',
            field=models.ManyToManyField(to='shop.Option', verbose_name='Options', blank=True),
        ),
        migrations.AddField(
            model_name='wheelsize',
            name='real_type',
            field=models.ForeignKey(editable=False, to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='wheelsize',
            name='site',
            field=models.ForeignKey(verbose_name='site', blank=True, to='sites.Site'),
        ),
        migrations.AddField(
            model_name='wheelsize',
            name='tax',
            field=models.ManyToManyField(to='shop.TaxClass', verbose_name='tax', blank=True),
        ),
        migrations.AddField(
            model_name='wheelsize',
            name='wheel',
            field=models.ForeignKey(related_name='sizes', verbose_name='wheel', to='kx.Wheel'),
        ),
        migrations.AddField(
            model_name='wheelreview',
            name='reviewee',
            field=models.ForeignKey(related_name='reviews', verbose_name='reviewee', to='kx.Wheel'),
        ),
        migrations.AddField(
            model_name='wheelreview',
            name='reviewer',
            field=models.ForeignKey(related_name='wheel_reviews', verbose_name='reviewer', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='wheelpicturethumbnail',
            name='wheelpicture',
            field=models.ForeignKey(related_name='thumbnails', to='kx.WheelPicture'),
        ),
        migrations.AddField(
            model_name='wheelpicture',
            name='wheel',
            field=models.ForeignKey(related_name='pictures', verbose_name='wheel', to='kx.Wheel'),
        ),
        migrations.AddField(
            model_name='wheelmanufacturerdiscount',
            name='manufacturer',
            field=models.ForeignKey(related_name='discounts', verbose_name='manufacturer', to='kx.WheelManufacturer'),
        ),
        migrations.AddField(
            model_name='wheelmanufacturerdiscount',
            name='user',
            field=models.ForeignKey(related_name='wheel_discounts', verbose_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='wheelcustomermedia',
            name='user',
            field=models.ForeignKey(related_name='wheel_media', verbose_name='uploader', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='wheelcustomermedia',
            name='wheel',
            field=models.ForeignKey(related_name='customer_media', to='kx.Wheel'),
        ),
        migrations.AddField(
            model_name='wheelcoupon',
            name='wheel',
            field=models.ForeignKey(related_name='coupons', to='kx.Wheel'),
        ),
        migrations.AddField(
            model_name='wheel',
            name='manufacturer',
            field=models.ForeignKey(related_name='wheels', verbose_name='manufacturer', to='kx.WheelManufacturer'),
        ),
        migrations.AddField(
            model_name='tiresize',
            name='options',
            field=models.ManyToManyField(to='shop.Option', verbose_name='Options', blank=True),
        ),
        migrations.AddField(
            model_name='tiresize',
            name='real_type',
            field=models.ForeignKey(editable=False, to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='tiresize',
            name='site',
            field=models.ForeignKey(verbose_name='site', blank=True, to='sites.Site'),
        ),
        migrations.AddField(
            model_name='tiresize',
            name='tax',
            field=models.ManyToManyField(to='shop.TaxClass', verbose_name='tax', blank=True),
        ),
        migrations.AddField(
            model_name='tiresize',
            name='tire',
            field=models.ForeignKey(related_name='sizes', verbose_name='tire', to='kx.Tire'),
        ),
        migrations.AddField(
            model_name='tirereview',
            name='reviewee',
            field=models.ForeignKey(related_name='reviews', verbose_name='reviewee', to='kx.Tire'),
        ),
        migrations.AddField(
            model_name='tirereview',
            name='reviewer',
            field=models.ForeignKey(related_name='tire_reviews', verbose_name='reviewer', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='tirepicturethumbnail',
            name='tirepicture',
            field=models.ForeignKey(related_name='thumbnails', to='kx.TirePicture'),
        ),
        migrations.AddField(
            model_name='tirepicture',
            name='tire',
            field=models.ForeignKey(related_name='pictures', verbose_name='tire', to='kx.Tire'),
        ),
        migrations.AddField(
            model_name='tiremanufacturerdiscount',
            name='manufacturer',
            field=models.ForeignKey(related_name='discounts', verbose_name='manufacturer', to='kx.TireManufacturer'),
        ),
        migrations.AddField(
            model_name='tiremanufacturerdiscount',
            name='user',
            field=models.ForeignKey(related_name='tire_discounts', verbose_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tirecustomermedia',
            name='tire',
            field=models.ForeignKey(related_name='customer_media', to='kx.Tire'),
        ),
        migrations.AddField(
            model_name='tirecustomermedia',
            name='user',
            field=models.ForeignKey(related_name='tire_media', verbose_name='uploader', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tirecoupon',
            name='tire',
            field=models.ForeignKey(related_name='coupons', to='kx.Tire'),
        ),
        migrations.AddField(
            model_name='tirecategory',
            name='parent',
            field=models.ForeignKey(related_name='children', blank=True, to='kx.TireCategory', null=True),
        ),
        migrations.AddField(
            model_name='tire',
            name='category',
            field=models.ForeignKey(related_name='tires', verbose_name='category', to='kx.TireCategory'),
        ),
        migrations.AddField(
            model_name='tire',
            name='manufacturer',
            field=models.ForeignKey(related_name='tires', verbose_name='manufacturer', to='kx.TireManufacturer'),
        ),
        migrations.AddField(
            model_name='dealerwheelmanufacturerdiscount',
            name='manufacturer',
            field=models.ForeignKey(related_name='dealer_discounts', verbose_name='manufacturer', to='kx.WheelManufacturer'),
        ),
        migrations.AddField(
            model_name='dealerwheelmanufacturerdiscount',
            name='user',
            field=models.ForeignKey(related_name='dealer_wheel_discounts', verbose_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='dealertiremanufacturerdiscount',
            name='manufacturer',
            field=models.ForeignKey(related_name='dealer_discounts', verbose_name='manufacturer', to='kx.TireManufacturer'),
        ),
        migrations.AddField(
            model_name='dealertiremanufacturerdiscount',
            name='user',
            field=models.ForeignKey(related_name='dealer_tire_discounts', verbose_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='dealeraccessoriesdiscount',
            name='accessories',
            field=models.ForeignKey(related_name='dealer_discounts', verbose_name='manufacturer', to='kx.Accessories'),
        ),
        migrations.AddField(
            model_name='dealeraccessoriesdiscount',
            name='user',
            field=models.ForeignKey(related_name='dealer_accesories_discounts', verbose_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='accessoriesreview',
            name='reviewee',
            field=models.ForeignKey(related_name='reviews', verbose_name='reviewee', to='kx.AccessoriesList'),
        ),
        migrations.AddField(
            model_name='accessoriesreview',
            name='reviewer',
            field=models.ForeignKey(related_name='accessories_reviews', verbose_name='reviewer', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='accessoriespicturethumbnail',
            name='wheelpicture',
            field=models.ForeignKey(related_name='thumbnails', to='kx.AccessoriesPicture'),
        ),
        migrations.AddField(
            model_name='accessoriespicture',
            name='wheel',
            field=models.ForeignKey(related_name='pictures', verbose_name='accessories_list', to='kx.AccessoriesList'),
        ),
        migrations.AddField(
            model_name='accessorieslist',
            name='manufacturer',
            field=models.ForeignKey(related_name='accessories', verbose_name='accessories', to='kx.Accessories'),
        ),
        migrations.AddField(
            model_name='accessoriesdiscount',
            name='accesories',
            field=models.ForeignKey(related_name='discounts', verbose_name='accesories', to='kx.Accessories'),
        ),
        migrations.AddField(
            model_name='accessoriesdiscount',
            name='user',
            field=models.ForeignKey(related_name='accesories_discounts', verbose_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='accessoriesdetail',
            name='accessories_list',
            field=models.ForeignKey(related_name='sizes', verbose_name='accessories list', to='kx.AccessoriesList'),
        ),
        migrations.AddField(
            model_name='accessoriesdetail',
            name='options',
            field=models.ManyToManyField(to='shop.Option', verbose_name='Options', blank=True),
        ),
        migrations.AddField(
            model_name='accessoriesdetail',
            name='real_type',
            field=models.ForeignKey(editable=False, to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='accessoriesdetail',
            name='site',
            field=models.ForeignKey(verbose_name='site', blank=True, to='sites.Site'),
        ),
        migrations.AddField(
            model_name='accessoriesdetail',
            name='tax',
            field=models.ManyToManyField(to='shop.TaxClass', verbose_name='tax', blank=True),
        ),
        migrations.AddField(
            model_name='accessoriescustomermedia',
            name='accessorie',
            field=models.ForeignKey(related_name='customer_media', to='kx.AccessoriesList'),
        ),
        migrations.AddField(
            model_name='accessoriescustomermedia',
            name='user',
            field=models.ForeignKey(related_name='accessorie_media', verbose_name='uploader', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='accessoriescoupon',
            name='wheel',
            field=models.ForeignKey(related_name='coupons', to='kx.AccessoriesList'),
        ),
        migrations.AlterUniqueTogether(
            name='wheelsize',
            unique_together=set([('wheel', 'sku')]),
        ),
        migrations.AlterUniqueTogether(
            name='tire',
            unique_together=set([('manufacturer', 'name')]),
        ),
    ]

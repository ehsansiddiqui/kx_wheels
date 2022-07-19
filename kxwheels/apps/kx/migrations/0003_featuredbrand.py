# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('kx', '0002_auto_20190702_1054'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeaturedBrand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('meta_title', models.CharField(max_length=255, null=True, verbose_name='meta title', blank=True)),
                ('meta_keywords', models.CharField(max_length=255, null=True, verbose_name='meta keywords', blank=True)),
                ('meta_description', models.CharField(max_length=500, null=True, verbose_name='meta description', blank=True)),
                ('ordering', models.IntegerField(null=True, verbose_name='sort order', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at', null=True)),
                ('is_active', models.BooleanField(default=1, verbose_name='is active?')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('slug', models.SlugField(max_length=255, verbose_name='slug', blank=True)),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('is_configurator', models.BooleanField(default=False, verbose_name='is configurator available')),
                ('picture', sorl.thumbnail.fields.ImageField(upload_to=b'media/manufacturers', null=True, verbose_name='picture', blank=True)),
                ('warranty', models.TextField(null=True, verbose_name='warranty', blank=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Featured Brand',
                'verbose_name_plural': 'Featured Brands',
            },
        ),
    ]

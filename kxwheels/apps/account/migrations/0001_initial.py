# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dealer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('business_name', models.CharField(max_length=255, verbose_name='business name')),
                ('contact_name', models.CharField(max_length=255, verbose_name='contact name')),
                ('street_address', models.CharField(max_length=255, verbose_name='streeet address', blank=True)),
                ('city', models.CharField(max_length=255, verbose_name='city', blank=True)),
                ('postal_code', models.CharField(max_length=20, verbose_name='postal/zip code', blank=True)),
                ('province', models.CharField(max_length=255, verbose_name='province', blank=True)),
                ('country', models.CharField(max_length=255, verbose_name='country', blank=True)),
                ('email', models.EmailField(max_length=255, verbose_name='email')),
                ('business_phone', models.CharField(max_length=20, verbose_name='business phone')),
                ('other_phone', models.CharField(max_length=20, null=True, verbose_name='other phone', blank=True)),
                ('heard', models.TextField(max_length=500, verbose_name='where did you hear about us?')),
                ('business_kind', models.IntegerField(verbose_name='what kind of business do you have?', choices=[(1, b'Tire shop'), (2, b'Custom wheel shop'), (3, b'Online business'), (4, b'Other')])),
                ('business_kind_other', models.CharField(max_length=500, null=True, verbose_name='business other', blank=True)),
                ('interested_in', models.TextField(max_length=500, verbose_name='what products are you interested in?')),
                ('volume', models.TextField(max_length=500, verbose_name='What do you expect your monthly volume to be?')),
                ('comments', models.TextField(max_length=500, verbose_name='comments')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
            ],
        ),
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('access_key', models.CharField(max_length=32, blank=True)),
                ('secret_key', models.CharField(max_length=64, blank=True)),
                ('is_active', models.BooleanField()),
                ('site', models.ForeignKey(related_name='developer_profile', verbose_name='site', blank=True, to='sites.Site')),
                ('user', models.OneToOneField(related_name='developer_profile', verbose_name='developer', blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Personal, Work, etc', max_length=255, verbose_name='profile name')),
                ('first_name', models.CharField(max_length=255, verbose_name='first name')),
                ('last_name', models.CharField(max_length=255, verbose_name='last name')),
                ('landline_phone', models.CharField(max_length=16, verbose_name='landline phone')),
                ('cell_phone', models.CharField(max_length=16, null=True, verbose_name='cell phone', blank=True)),
                ('fax', models.CharField(max_length=16, null=True, verbose_name='fax', blank=True)),
                ('address_1', models.CharField(max_length=255, verbose_name='address 1', blank=True)),
                ('address_2', models.CharField(max_length=255, verbose_name='address 2', blank=True)),
                ('city', models.CharField(max_length=255, verbose_name='city', blank=True)),
                ('postal_code', models.CharField(max_length=20, verbose_name='postal/zip code', blank=True)),
                ('province', models.CharField(max_length=255, verbose_name='province', blank=True)),
                ('country', models.CharField(max_length=255, verbose_name='country', blank=True)),
                ('subdomain', models.CharField(max_length=50, unique=True, null=True, verbose_name='subdomain', blank=True)),
                ('dealer_logo', models.ImageField(upload_to=b'media/dealer_logo', null=True, verbose_name='dealer_logo', blank=True)),
                ('banner', models.ImageField(upload_to=b'media/banner', null=True, verbose_name='banner', blank=True)),
                ('site', models.ForeignKey(related_name='profiles', verbose_name='site', blank=True, to='sites.Site', null=True)),
                ('user', models.ForeignKey(related_name='profiles', verbose_name='customer', blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='profile',
            unique_together=set([('user', 'name')]),
        ),
    ]

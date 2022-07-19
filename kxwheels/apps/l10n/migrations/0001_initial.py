# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminArea',
            fields=[
                ('iso_3166_2', models.CharField(max_length=128, serialize=False, verbose_name='ISO 3166-2 Postal Abbreviation', primary_key=True, blank=True)),
                ('name', models.CharField(max_length=60, verbose_name='admin area name')),
                ('active', models.BooleanField(default=True, verbose_name='is active')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'administrative area',
                'verbose_name_plural': 'administrative areas',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='city name')),
                ('iso_3166_2', models.ForeignKey(to='l10n.AdminArea')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': 'cities',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('iso_3166_1', models.CharField(max_length=10, serialize=False, verbose_name='ISO 3166-1 alpha-2', primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='official name')),
                ('formal_name', models.CharField(max_length=128, verbose_name='formal name')),
                ('active', models.BooleanField(default=True, verbose_name='is active')),
                ('continent', models.CharField(blank=True, max_length=2, null=True, verbose_name='continent', choices=[(b'AF', 'Africa'), (b'NA', 'North America'), (b'EU', 'Europe'), (b'AS', 'Asia'), (b'OC', 'Oceania'), (b'SA', 'South America'), (b'AN', 'Antarctica')])),
                ('admin_area', models.CharField(blank=True, max_length=128, null=True, verbose_name='administrative area', choices=[(b'a', 'Another'), (b'i', 'Island'), (b'ar', 'Arrondissement'), (b'at', 'Atoll'), (b'ai', 'Autonomous island'), (b'ca', 'Canton'), (b'cm', 'Commune'), (b'co', 'County'), (b'dp', 'Department'), (b'de', 'Dependency'), (b'dt', 'District'), (b'dv', 'Division'), (b'em', 'Emirate'), (b'gv', 'Governorate'), (b'ic', 'Island council'), (b'ig', 'Island group'), (b'ir', 'Island region'), (b'kd', 'Kingdom'), (b'mu', 'Municipality'), (b'pa', 'Parish'), (b'pf', 'Prefecture'), (b'pr', 'Province'), (b'rg', 'Region'), (b'rp', 'Republic'), (b'sh', 'Sheading'), (b'st', 'State'), (b'sd', 'Subdivision'), (b'sj', 'Subject'), (b'ty', 'Territory')])),
                ('postal_type', models.CharField(blank=True, max_length=128, null=True, verbose_name='postal type', choices=[(b'postal_code', b'Postal Code'), (b'zip', b'Zip Code'), (b'postcode', b'Postcode')])),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'country',
                'verbose_name_plural': 'countries',
            },
        ),
        migrations.CreateModel(
            name='PostalCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('postal_code', models.CharField(unique=True, max_length=10, verbose_name='postal code')),
                ('location', models.CharField(max_length=40, null=True, verbose_name='location point', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('city', models.ForeignKey(to='l10n.City')),
                ('iso_3166_2', models.ForeignKey(to='l10n.AdminArea')),
            ],
        ),
        migrations.AddField(
            model_name='adminarea',
            name='iso_3166_1',
            field=models.ForeignKey(to='l10n.Country'),
        ),
        migrations.AlterUniqueTogether(
            name='adminarea',
            unique_together=set([('iso_3166_1', 'iso_3166_2')]),
        ),
    ]

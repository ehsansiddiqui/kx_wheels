# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kx', '0003_featuredbrand'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FeaturedBrand',
        ),
    ]

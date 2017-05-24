# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issue', '0002_auto_20170518_2349'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='claimusers',
            field=models.TextField(default=b'', blank=True),
        ),
    ]

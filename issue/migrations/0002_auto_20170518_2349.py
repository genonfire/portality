# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issue', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='count',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='issue',
            name='email',
            field=models.CharField(max_length=b'50', blank=True),
        ),
    ]

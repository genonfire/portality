# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('giza', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='giza',
            name='belongto',
            field=models.CharField(max_length=b'20', blank=True),
        ),
        migrations.AlterField(
            model_name='giza',
            name='facebook',
            field=models.CharField(max_length=b'50', blank=True),
        ),
        migrations.AlterField(
            model_name='giza',
            name='twitter',
            field=models.CharField(max_length=b'50', blank=True),
        ),
    ]

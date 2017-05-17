# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.CharField(max_length=b'50')),
                ('subject', models.CharField(max_length=b'100')),
                ('url', models.CharField(max_length=b'255')),
                ('archive', models.CharField(max_length=b'255', blank=True)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('count', models.IntegerField(default=0)),
            ],
        ),
    ]

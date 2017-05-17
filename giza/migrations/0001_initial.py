# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Giza',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=b'30')),
                ('email', models.CharField(max_length=b'50')),
                ('twitter', models.CharField(max_length=b'50')),
                ('facebook', models.CharField(max_length=b'50')),
                ('belongto', models.CharField(max_length=b'20')),
                ('portrait', models.ImageField(upload_to=b'portrait/', blank=True)),
                ('profile', models.TextField(blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True)),
            ],
        ),
    ]

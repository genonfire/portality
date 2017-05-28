# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issue', '0003_issue_claimusers'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='goodcount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='issue',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-18 17:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0035_auto_20180118_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='hltbLength',
            field=models.FloatField(blank=True, max_length=255, null=True),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-18 18:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0036_auto_20180118_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='releaseDate',
            field=models.DateField(blank=True, max_length=255, null=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-10 12:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0007_auto_20170810_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='finishedAt',
            field=models.DateField(blank=True, null=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-24 08:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0008_auto_20170810_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='userScore',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-18 22:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0037_auto_20180118_1816'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='beated',
            field=models.BooleanField(default=False),
        ),
    ]
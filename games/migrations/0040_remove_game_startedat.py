# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-22 13:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0039_auto_20180118_2238'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='startedAt',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2020-02-10 00:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0050_auto_20200208_1123'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='beaten',
        ),
        migrations.RemoveField(
            model_name='game',
            name='stopped_playing_at',
        ),
    ]

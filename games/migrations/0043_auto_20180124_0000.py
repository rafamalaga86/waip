# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-24 00:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0042_auto_20180122_1851'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='game',
            unique_together=set([('id', 'name')]),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-25 15:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0018_auto_20170825_1540'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='hltbLength',
        ),
    ]

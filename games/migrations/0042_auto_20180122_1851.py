# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-22 18:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0041_auto_20180122_1849'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='modifiedAt',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='note',
            old_name='createdAt',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='note',
            old_name='modifiedAt',
            new_name='updated_at',
        ),
    ]

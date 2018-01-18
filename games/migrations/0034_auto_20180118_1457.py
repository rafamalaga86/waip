# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-18 14:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0033_auto_20180117_0924'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='note',
            name='modifiedAt',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
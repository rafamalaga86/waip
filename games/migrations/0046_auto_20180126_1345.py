# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-26 13:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0045_game_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='order',
            field=models.IntegerField(default=10),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-25 15:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0019_remove_game_hltblength'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='hltbLength',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

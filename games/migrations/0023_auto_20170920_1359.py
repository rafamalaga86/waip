# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-20 13:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0022_remove_game_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='hltbUrl',
        ),
        migrations.RemoveField(
            model_name='game',
            name='metacriticUrl',
        ),
        migrations.RemoveField(
            model_name='game',
            name='metacriticUserScore',
        ),
        migrations.RemoveField(
            model_name='game',
            name='userScore',
        ),
        migrations.AlterField(
            model_name='game',
            name='coverUrl',
            field=models.URLField(default='https://howlongtobeat.com/gameimages/Pony_Island_header.jpg', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='game',
            name='startedAt',
            field=models.DateField(blank=True, null=True),
        ),
    ]
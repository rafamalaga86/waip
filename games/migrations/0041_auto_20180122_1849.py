# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-22 18:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0040_remove_game_startedat'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='coverUrl',
            new_name='cover_url',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='createdAt',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='hltbLength',
            new_name='hltb_length',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='metacriticScore',
            new_name='metacritic_score',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='releaseDate',
            new_name='release_date',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2020-02-08 11:23
from __future__ import unicode_literals

from django.db import migrations


def move_date_to_played(apps, schema_editor):
    Game = apps.get_model('games', 'Game')
    Played = apps.get_model('games', 'Played')

    for game in Game.objects.all():
        Played(stopped_playing_at=game.stopped_playing_at,
               beaten=game.beaten,
               created_at=game.created_at,
               updated_at=game.updated_at,
               game=game
               ).save()


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0049_played_beaten'),
    ]

    operations = [
        migrations.RunPython(move_date_to_played, reverse_code=migrations.RunPython.noop),
    ]
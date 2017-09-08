# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-25 14:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0009_game_userscore'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='coverUrl',
            field=models.URLField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='gameTimes',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='metacriticScore',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='metacriticUserScore',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='platforms',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='releaseDate',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='synopsis',
            field=models.TextField(null=True),
        ),
    ]
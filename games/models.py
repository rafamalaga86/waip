# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.conf import settings


class Game(models.Model):
    # Original
    name = models.CharField(max_length=255)
    order = models.IntegerField(default=10)  # The higier the more priority it has

    # Scrapped properties
    cover_url = models.URLField(max_length=255) 
    hltb_length = models.FloatField(max_length=255, blank=True, null=True)
    synopsis = models.TextField(blank=True, null=True)
    release_date = models.DateField(max_length=255, blank=True, null=True)
    developer = models.CharField(max_length=255, blank=True, null=True)
    genres = models.CharField(max_length=255, blank=True, null=True)
    metacritic_score = models.CharField(max_length=255, blank=True, null=True)

    # Meta properties
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Relationships
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('user', 'name')


class Played(models.Model):
    stopped_playing_at = models.DateField(blank=True, null=True)
    beaten = models.BooleanField(default=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    # Meta properties
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.game.name + (' at ' + self.stopped_playing_at.strftime('%m/%d/%Y')
                                 if self.stopped_playing_at is not None else ' Jugando')


class Note(models.Model):
    text = models.TextField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    # Meta properties
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.game.name + ': ' + self.text

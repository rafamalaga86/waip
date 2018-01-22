# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Game(models.Model):
    # Original
    name = models.CharField(max_length=255)
    stopped_playing_at = models.DateField(blank=True, null=True)
    beaten = models.BooleanField(default=False)

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

    def clean(self):
        if self.beaten and not self.stopped_playing_at:
            raise ValidationError('If you mark game as beaten, you should put a Finish Date \
                (even when is not an accurate date, we want to allocate it to a year)')


class Note(models.Model):
    text = models.TextField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    # Meta properties
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.game.name + ': ' + self.text

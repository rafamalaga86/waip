# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Game(models.Model):
    # Django model properties
    name = models.CharField(max_length=255, unique=True)
    metacriticUrl = models.URLField(max_length=255, null=True)
    hltbUrl = models.URLField(max_length=255, null=True)
    startedAt = models.DateField(auto_now_add=True)
    finishedAt = models.DateField(blank=True, null=True)
    userScore = models.PositiveSmallIntegerField(blank=True, null=True)

    # Meta properties
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    # Injected properties in execution time
    coverUrl = None
    gameTimes = None
    synopsis = None
    releaseDate = None
    platforms = None
    metacriticScore = None
    metacriticUserScore = None

    # def __str__(self):
    #     return self.name

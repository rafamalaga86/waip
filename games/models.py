# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import requests
from bs4 import BeautifulSoup
import os
from games.utils import getMetacriticScoreColour


class Game(models.Model):
    # Original
    name = models.CharField(max_length=255, unique=True)
    startedAt = models.DateField(blank=True, null=True)
    finishedAt = models.DateField(blank=True, null=True)

    # Scrapped properties
    coverUrl = models.URLField(max_length=255)
    hltbLength = models.CharField(max_length=255, blank=True, null=True)
    synopsis = models.TextField(blank=True, null=True)
    releaseDate = models.CharField(max_length=255, blank=True, null=True)
    developer = models.CharField(max_length=255, blank=True, null=True)
    genres = models.CharField(max_length=255, blank=True, null=True)
    metacriticScore = models.CharField(max_length=255, blank=True, null=True)

    # Meta properties
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    # Injected properties
    metacriticScoreColour = None
    metacriticUserScoreColour = None

    def __str__(self):
        return self.name

    def injectData(self):
        self.metacriticScoreColour = getMetacriticScoreColour(self.metacriticScore)

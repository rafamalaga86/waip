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
    metacriticUrl = models.URLField(max_length=255, null=True)
    hltbUrl = models.URLField(max_length=255, null=True)
    startedAt = models.DateField(auto_now_add=True)
    finishedAt = models.DateField(blank=True, null=True)
    userScore = models.PositiveSmallIntegerField(blank=True, null=True)

    # Scrapped properties
    coverUrl = models.URLField(max_length=255, blank=True, null=True)
    image = models.ImageField(blank=True)
    hltbLength = models.CharField(max_length=255, blank=True, null=True)
    synopsis = models.TextField(blank=True, null=True)
    releaseDate = models.CharField(max_length=255, blank=True, null=True)
    developer = models.CharField(max_length=255, blank=True, null=True)
    genres = models.CharField(max_length=255, blank=True, null=True)
    metacriticScore = models.CharField(max_length=255, blank=True, null=True)
    metacriticUserScore = models.CharField(max_length=255, blank=True, null=True)

    # Meta properties
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    # Injected properties
    metacriticScoreColour = None
    metacriticUserScoreColour = None

    # Class constants
    HLTB_SA = 'https://howlongtobeat.com/'  # Scheme and Authority of URL
    SCRAPPED_PROPERTIES = (
        'coverUrl',
        'hltbLength',
        'synopsis',
        'releaseDate',
        'developer',
        'genres',
        'metacriticScore',
        'metacriticUserScore',
    )

    def __str__(self):
        return self.name

    def injectData(self):
        for property_ in self.SCRAPPED_PROPERTIES:
            if getattr(self, property_) is None:
                self._scrapData()
        self.metacriticScoreColour = getMetacriticScoreColour(self.metacriticScore)
        self.metacriticUserScoreColour = getMetacriticScoreColour(self.metacriticUserScore)

    def _scrapData(self):
        metacriticRequest = requests.get(self.metacriticUrl, headers={'User-Agent': 'Mozilla/5.0'})
        hltbRequest = requests.get(self.hltbUrl)

        # if (metacriticRequest.status_code != 200 or hltbRequest.status_code != 200):
        #     return HttpResponse('The scrap to metacritic or HLTB does not work', status=500)

        metacriticSoup = BeautifulSoup(metacriticRequest.text)
        hltbSoup = BeautifulSoup(hltbRequest.text)

        # HLTB Scrap
        if self.coverUrl is None:
            self.coverUrl = os.path.join(
                self.HLTB_SA,
                hltbSoup.find('div', class_="game_image").find('img').get('src')
            )

        # if self.gameTimes is None:
        #     gameTimes = hltbSoup.find('div', class_="game_times").findAll('li')
        #     self.gameTimes = {
        #         'mainStory': gameTimes[0].find('div').text.strip(),
        #         'mainPlusExtras': gameTimes[1].find('div').text.strip(),
        #         'completionist': gameTimes[2].find('div').text.strip(),
        #         'allStyles': gameTimes[3].find('div').text.strip()
        #     }

        if self.hltbLength is None:
            gameTimes = hltbSoup.find('div', class_="game_times").findAll('li')
            self.hltbLength = gameTimes[0].find('div').text.strip()

        if self.synopsis is None:
            self.synopsis = hltbSoup.find('div', class_='profile_header_alt').text.strip()

        # Metacritic Scrap
        if self.developer is None:
            self.developer = metacriticSoup.find(class_='summary_detail developer') \
                .find(class_='data').text.strip()

        if self.genres is None:
            self.genres = metacriticSoup.find(class_='summary_detail product_genre') \
                .find(class_='data').text.strip()

        if self.releaseDate is None:
            self.releaseDate = metacriticSoup.find(class_='summary_detail release_data') \
                .find(class_='data').text.strip()

        if self.metacriticScore is None:
            self.metacriticScore = metacriticSoup.select('div.metascore_w.xlarge > span')[0] \
                .text.strip()

        if self.metacriticUserScore is None:
            self.metacriticUserScore = metacriticSoup.select('div.metascore_w.user.large')[0] \
                .text.strip()

        self.save()

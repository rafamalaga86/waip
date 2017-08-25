# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import requests
from bs4 import BeautifulSoup
import os

HLTB_SA = 'https://howlongtobeat.com/'  # Scheme and Authority of URL


class Game(models.Model):
    # Django model properties
    name = models.CharField(max_length=255, unique=True)
    metacriticUrl = models.URLField(max_length=255, null=True)
    hltbUrl = models.URLField(max_length=255, null=True)
    startedAt = models.DateField(auto_now_add=True)
    finishedAt = models.DateField(blank=True, null=True)
    userScore = models.PositiveSmallIntegerField(blank=True, null=True)

    # Injected properties in execution time
    coverUrl = None
    gameTimes = None
    synopsis = None
    releaseDate = None
    platforms = None
    metacriticScore = None
    metacriticUserScore = None

    # Meta properties
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.name

    def injectScrappedData(self):
        metacriticRequest = requests.get(self.metacriticUrl, headers={'User-Agent': 'Mozilla/5.0'})
        hltbRequest = requests.get(self.hltbUrl)

        # if (metacriticRequest.status_code != 200 or hltbRequest.status_code != 200):
        #     return HttpResponse('The scrap to metacritic or HLTB does not work', status=500)

        metacriticSoup = BeautifulSoup(metacriticRequest.text)
        hltbSoup = BeautifulSoup(hltbRequest.text)

        # HLTB Scrap
        self.coverUrl = os.path.join(
            HLTB_SA,
            hltbSoup.find('div', class_="game_image").find('img').get('src')
        )

        gameTimesSoup = hltbSoup.find('div', class_="game_times").findAll('li')
        self.gameTimes = {
            'mainStory': gameTimesSoup[0].find('div').text,
            'mainPlusExtras': gameTimesSoup[1].find('div').text,
            'completionist': gameTimesSoup[2].find('div').text,
            'allStyles': gameTimesSoup[3].find('div').text
        }

        self.synopsis = hltbSoup.find('div', class_='profile_header_alt').text.strip()

        # Metacritic Scrap
        self.developer = metacriticSoup.find(class_='summary_detail developer') \
            .find(class_='data').text
        self.genres = metacriticSoup.find(class_='summary_detail product_genre') \
            .find(class_='data').text
        self.releaseDate = metacriticSoup.find(class_='summary_detail release_data') \
            .find(class_='data').text
        self.metacriticScore = metacriticSoup.select('div.metascore_w.xlarge > span')[0].text
        self.metacriticUserScore = metacriticSoup.select('div.metascore_w.user.large')[0].text

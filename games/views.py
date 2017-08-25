# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Game
from bs4 import BeautifulSoup
from django.shortcuts import HttpResponse
from django.template import loader
import requests
import os

from pprint import pprint

HLTB_SA = 'https://howlongtobeat.com/'  # Scheme and Authority of URL


def helloWorld(request):
    # return HttpResponse('HELLO WORLD')
    # return render(request, 'index.html')
    games = Game.objects.order_by('id')
    template = loader.get_template('example.html')
    context = {
        'games': games
    }

    return HttpResponse(template.render(context, request))


def main(request):
    games = Game.objects.order_by('startedAt')

    for game in games:
        metacriticRequest = requests.get(
            game.metacriticUrl,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        hltbRequest = requests.get(game.hltbUrl)

        if (metacriticRequest.status_code != 200 or hltbRequest.status_code != 200):
            return HttpResponse('The scrap to metacritic or HLTB does not work', status=500)

        metacriticSoup = BeautifulSoup(metacriticRequest.text)
        hltbSoup = BeautifulSoup(hltbRequest.text)

        # HLTB Scrap
        game.coverUrl = os.path.join(
            HLTB_SA,
            hltbSoup.find('div', class_="game_image").find('img').get('src')
        )

        gameTimesSoup = hltbSoup.find('div', class_="game_times").findAll('li')
        game.gameTimes = {
            'mainStory': gameTimesSoup[0].find('div').text,
            'mainPlusExtras': gameTimesSoup[1].find('div').text,
            'completionist': gameTimesSoup[2].find('div').text,
            'allStyles': gameTimesSoup[3].find('div').text
        }

        game.synopsis = hltbSoup.find('div', class_='profile_header_alt').text.strip()

        # Metacritic Scrap
        game.developer = metacriticSoup.find(class_='summary_detail developer') \
            .find(class_='data').text
        game.genres = metacriticSoup.find(class_='summary_detail product_genre') \
            .find(class_='data').text
        game.releaseDate = metacriticSoup.find(class_='summary_detail release_data') \
            .find(class_='data').text
        game.metacriticScore = metacriticSoup.select('div.metascore_w.xlarge > span')[0].text
        game.metacriticUserScore = metacriticSoup.select('div.metascore_w.user.large')[0].text

    context = {
        'games': games,
        'title': 'What is Postizo playing'
    }

    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))

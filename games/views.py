# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Game
from django.shortcuts import HttpResponse
from django.template import loader

from pprint import pprint


def main(request):
    # Retrieve list of non finished games ID's to pass them to the frontend
    ids = Game.objects.filter(finishedAt=None).values_list('id', flat=True)

    context = {
        'ids': ids,
    }

    template = loader.get_template('home.html')
    return HttpResponse(template.render(context, request))


def simpleList(request, id):
    # return HttpResponse('HELLO WORLD')
    # return render(request, 'home.html')
    games = Game.objects.order_by('id')
    template = loader.get_template('example.html')
    context = {
        'games': games
    }

    return HttpResponse(template.render(context, request))


def getGameAjax(request, id):
    # Raise Exception()
    game = Game.objects.get(pk=id)
    game.injectData()

    context = {
        'game': game,
        'userScoreColour': game.metacriticScoreColour,
    }

    template = loader.get_template('ajax/game.html')
    return HttpResponse(template.render(context, request))

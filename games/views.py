# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponseBadRequest, \
    JsonResponse
from django.shortcuts import HttpResponse, Http404, get_object_or_404
from django.template import loader
from django.conf import settings
from django.views import View
from .models import Game
from .forms import GameForm, ScrapGameForm
from games.utils import GameScrapper
import datetime

# import json


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
    context = {
        'games': games
    }

    template = loader.get_template('example.html')
    return HttpResponse(template.render(context, request))


def newGame(request):
    # POST ----------------------------------------------
    if request.method == 'POST':
        postedGame = GameForm(request.POST)
        if postedGame.is_valid():
            postedGame.save()
            return HttpResponseRedirect('/')

    # GET -----------------------------------------------
    context = {
        'gameForm': GameForm,
        'scrapGameForm': ScrapGameForm,
    }

    template = loader.get_template('new-game.html')
    return HttpResponse(template.render(context, request))


def finishGameAjax(request, id):
    game = Game.objects.get(pk=id)

    if game.finishedAt is not None:
        return HttpResponseForbidden('The game already has a "finishedAt" date.')

    game.finishedAt = datetime.date.today()
    game.save()
    return HttpResponse('')  # I just want to give a 200


def getGameAjax(request, id):
    if not settings.DEBUG and not request.is_ajax():
        return HttpResponseForbidden()

    # equivalent to get_object_or_404(Game, pk=id)
    try:
        game = Game.objects.get(pk=id)
    except Game.DoesNotExist:
        raise Http404('That game was not found.')

    game.injectData()

    context = {
        'game': game,
    }

    template = loader.get_template('ajax/game.html')
    return HttpResponse(template.render(context, request))


def gameScrapAjax(request):
    if not settings.DEBUG and not request.is_ajax():
        return HttpResponseForbidden()

    form = ScrapGameForm(request.GET)

    if not form.is_valid():
        return HttpResponseBadRequest()

    formData = form.cleaned_data
    gameScrapper = GameScrapper(formData['metacriticUrl'], formData['hltbUrl'])
    gameDict = gameScrapper.getGame()

    return JsonResponse(gameDict)


class GameDetailView(View):
    def get(self, request, id):
        game = get_object_or_404(Game, pk=id)
        game.injectData()

        context = {
            'game': game,
        }

        template = loader.get_template('ajax/game.html')
        return HttpResponse(template.render(context, request))

    # def patch(self, request, id):
    #     game = get_object_or_404(Game, pk=id)
    #     # game.

    #     # TODO: Modify the object and save it

    #     return HttpResponseRedirect(request.path) # Redirect to GET

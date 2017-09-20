# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponseBadRequest, \
    JsonResponse
from django.shortcuts import HttpResponse, Http404, get_object_or_404
from django.template import loader
from django.conf import settings
from django.views import View
from .models import Game
from .forms import GameForm, ScrapMetacriticForm, ScrapHltbForm
from games.utils import ddg_scrapper, metacritic_scrapper, hltb_scrapper
import datetime

# import json


def home(request):
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


def scrap_metacritic_ajax(request):
    if not settings.DEBUG and not request.is_ajax():
        return HttpResponseForbidden()

    form = ScrapMetacriticForm(request.GET)

    if not form.is_valid():
        return HttpResponseBadRequest()

    formData = form.cleaned_data
    scrap_metacritic = metacritic_scrapper(formData['metacritic_url'])

    return JsonResponse(scrap_metacritic)


def scrap_hltb_ajax(request):
    if not settings.DEBUG and not request.is_ajax():
        return HttpResponseForbidden()

    form = ScrapHltbForm(request.GET)

    if not form.is_valid():
        return HttpResponseBadRequest()

    formData = form.cleaned_data
    scrap_hltb = hltb_scrapper(formData['hltb_url'])

    return JsonResponse(scrap_hltb)


def scrap_ddg_mc_ajax(request):
    if not settings.DEBUG and not request.is_ajax():
        return HttpResponseForbidden()

    keywords = 'site:metacritic.com '
    keywords += 'game '
    keywords += request.GET.get('keywords')

    result = ddg_scrapper(keywords)

    raise Exception(result)

    return JsonResponse(result)


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

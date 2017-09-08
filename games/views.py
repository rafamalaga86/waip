# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import HttpResponse, Http404
from django.template import loader
from django.conf import settings
from .models import Game
from .forms import GameForm

# from pprint import pprint


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
    # POST
    if request.method == 'POST':
        postedGame = GameForm(request.POST)
        if postedGame.is_valid():
            postedGame.save()
            return HttpResponseRedirect('/')

    # GET
    context = {
        'form': GameForm,
    }

    template = loader.get_template("new-game.html")
    return HttpResponse(template.render(context, request))


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

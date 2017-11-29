# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponseBadRequest, JsonResponse, \
    HttpResponseNotFound
from django.shortcuts import HttpResponse, get_object_or_404, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.forms.models import model_to_dict
from django.conf import settings
from django.views import View
from .models import Game
from .forms import GameForm, NoteForm, ScrapMetacriticForm, ScrapHltbForm
from games.utils import ddg_scrapper, metacritic_scrapper, hltb_scrapper
import datetime


def list_user_games(request):
    user = request.user if request.user.is_authenticated() else User.objects.get(pk=1)

    games = Game.objects.filter(user_id=user.id)
    for game in games.iterator():
        game.save()

    context = {
        'page': 'page-list',
        'games': games,
    }
    return render(request, 'game-grid.html', context)


@login_required
def add_game(request):
    # POST ----------------------------------------------
    if request.method == 'POST':
        game_form = GameForm(request.POST)
        if game_form.is_valid():
            game = game_form.save(commit=False)
            game.user = request.user
            game.save()
            return HttpResponseRedirect('/')

    # GET -----------------------------------------------
    else:
        game_form = GameForm()

    # SHARED --------------------------------------------
    context = {
        'page': 'page-add',
        'gameForm': game_form,
    }
    return render(request, 'new-game.html', context)


@login_required
def finishGameAjax(request, gameId):
    game = Game.objects.get(pk=gameId)

    if game.finishedAt is not None:
        return HttpResponseForbidden('The game already has a "finishedAt" date.')

    game.finishedAt = datetime.date.today()
    game.save()
    return HttpResponse('')  # I just want to give a 200


def getGameAjax(request, gameId):
    if not settings.DEBUG and not request.is_ajax():
        return HttpResponseForbidden()

    # equivalent to get_object_or_404(Game, pk=gameId)
    try:
        game = Game.objects.get(pk=gameId)
    except Game.DoesNotExist:
        return HttpResponseNotFound('That game was not found.')

    context = {
        'game': game,
    }
    return render(request, 'ajax/game.html', context)


@login_required
def add_note_to_game_ajax(request, gameId):
    # POST ----------------------------------------------
    if request.method == 'POST':
        # Check if the user has permission over the game
        noteForm = NoteForm(request.POST)
        if noteForm.is_valid():
            note = noteForm.save(commit=False)
            note.game = get_object_or_404(Game, pk=gameId)
            note.save()

    return JsonResponse(model_to_dict(note))


@login_required
def scrap_metacritic_ajax(request):
    if not settings.DEBUG and not request.is_ajax():
        return HttpResponseForbidden()

    form = ScrapMetacriticForm(request.GET)

    if not form.is_valid():
        return HttpResponseBadRequest()

    formData = form.cleaned_data
    scrap_metacritic = metacritic_scrapper(formData['metacritic_url'])

    return JsonResponse(scrap_metacritic)


@login_required
def scrap_hltb_ajax(request):
    if not settings.DEBUG and not request.is_ajax():
        return HttpResponseForbidden()

    form = ScrapHltbForm(request.GET)

    if not form.is_valid():
        return HttpResponseBadRequest()

    formData = form.cleaned_data
    scrap_hltb = hltb_scrapper(formData['hltb_url'])

    return JsonResponse(scrap_hltb)


class GameDetailView(View):
    @login_required
    def get(self, request, id):
        game = get_object_or_404(Game, pk=id)

        context = {
            'game': game,
        }
        return render(request, 'ajax/game.html', context)

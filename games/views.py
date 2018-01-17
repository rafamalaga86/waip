# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import QueryDict, HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.shortcuts import HttpResponse, get_object_or_404, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.forms.models import model_to_dict
from django.conf import settings
from django.views import View
from .models import Game, Note
from .forms import GameForm, NoteForm, ScrapMetacriticForm, ScrapHltbForm
from games.utils import metacritic_scrapper, hltb_scrapper
import datetime


def list_user_games(request):
    user = request.user if request.user.is_authenticated() else User.objects.get(pk=1)
    games = Game.objects.filter(user_id=user.id).order_by('-createdAt')
    return render(request, 'game-grid.html', {
        'page': 'page-list-games',
        'games': games,
    })


@login_required
def modify_game(request, gameId):
    # POST ----------------------------------------------
    if request.method == 'POST':
        game = None
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
    game = get_object_or_404(Game, pk=gameId)
    notes = Note.objects.filter(game=gameId)

    return render(request, 'game-detail.html', {
        'page': 'page-modify-game',
        'game': game,
        'game_form': game_form,
        'notes': notes,
    })


@login_required
def delete_game(request, gameId):
    get_object_or_404(Game, pk=gameId).delete()
    messages.success(request, 'The game was successfully deleted')
    return HttpResponseRedirect('/')


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
        'page': 'page-add-game',
        'game_form': game_form,
    }
    return render(request, 'new-game.html', context)


# AJAX CONTROLLERS
# ---------------------

@login_required
def finish_game_ajax(request, gameId):
    # TODO PATCH
    game = Game.objects.get(pk=gameId)

    if game.finishedAt is not None:
        return HttpResponseForbidden('The game already has a "finishedAt" date.')

    game.finishedAt = datetime.date.today()
    game.save()
    return HttpResponse('')  # I just want to give a 200


def get_game_ajax(request, gameId):
    if not settings.DEBUG and not request.is_ajax():
        return HttpResponseForbidden()

    context = {
        'game': get_object_or_404(Game, pk=gameId),
    }
    return render(request, 'ajax/game.html', context)


@login_required
def add_note_to_game_ajax(request, gameId):
    # POST ----------------------------------------------
    if request.method == 'POST':
        # Check if the user has permission over the game
        noteForm = NoteForm(request.POST)
        if not noteForm.is_valid():
            return HttpResponse(status=400)

        note = noteForm.save(commit=False)
        note.game = get_object_or_404(Game, pk=gameId)
        note.save()

    return JsonResponse(model_to_dict(note))


@login_required
def scrap_metacritic_ajax(request):
    if not settings.DEBUG and not request.is_ajax():
        return HttpResponseForbidden()

    scrap_metacritic_form = ScrapMetacriticForm(request.GET)

    if not scrap_metacritic_form.is_valid():
        return HttpResponse(status=400)

    formData = scrap_metacritic_form.cleaned_data
    scrap_metacritic = metacritic_scrapper(formData['metacritic_url'])

    return JsonResponse(scrap_metacritic)


@login_required
def scrap_hltb_ajax(request):
    if not settings.DEBUG and not request.is_ajax():
        return HttpResponseForbidden()

    scrap_hltb_form = ScrapHltbForm(request.GET)

    if not scrap_hltb_form.is_valid():
        return HttpResponse(status=400)

    formData = scrap_hltb_form.cleaned_data
    scrap_hltb = hltb_scrapper(formData['hltb_url'])

    return JsonResponse(scrap_hltb)


class NoteDetailAjaxView(LoginRequiredMixin, View):
    def put(self, request, gameId, noteId):
        note = get_object_or_404(Note, pk=noteId)
        noteForm = NoteForm(QueryDict(request.body))
        if not noteForm.is_valid():
            return HttpResponse(status=400)

        new_note = noteForm.save(commit=False)
        note.text = new_note.text
        note.save()
        return JsonResponse(model_to_dict(note))


    def delete(self, request, gameId, noteId):
        note = get_object_or_404(Note, pk=noteId)
        note.delete()
        return HttpResponse(status=204)

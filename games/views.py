# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .forms import GameForm, NoteForm, ScrapMetacriticForm, ScrapHltbForm
from .models import Game, Note
from datetime import date
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.http import QueryDict, HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.shortcuts import HttpResponse, get_object_or_404, render
from django.views import View
from games.utils import metacritic_scrapper, hltb_scrapper, get_menus_data
import logging

logger = logging.getLogger(__name__)

SHOWCASE_USER_ID = 1


def list_user_games(request):
    user = request.user if request.user.is_authenticated() else User.objects.get(id=SHOWCASE_USER_ID)

    # Get GET query string variables
    year = request.GET.get('year')
    beaten = request.GET.get('beaten', False)

    filters = {
        'user_id': user.id,
        'beaten': beaten,
    }
    if year is not None:
        filters['stopped_playing_at__year'] = year

    games = Game.objects.filter(**filters).order_by('-createdAt')

    for game in games:
        game.notes = Note.objects.filter(game_id=game.id).order_by('createdAt')

    return render(request, 'game-grid.html', {
        'page': 'page-list-games',
        'menu_data': get_menus_data(user.id),
        'games': games,
    })


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
        'menu_data': get_menus_data(request.user.id),
        'game_form': game_form,
    }
    return render(request, 'new-game.html', context)


@login_required
def modify_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    # Permission check
    if game.user.id != request.user.id:
        return HttpResponseForbidden('Don\'t be sneaky, you don\'t have permission over this game')

    # POST ----------------------------------------------
    if request.method == 'POST':
        game_form = GameForm(request.POST, instance=game)
        if game_form.is_valid():
            game.save()
            messages.success(request, 'The game was successfully updated')
            return HttpResponseRedirect('/')

    # GET -----------------------------------------------
    else:
        game_form = GameForm()

    # SHARED --------------------------------------------
    notes = Note.objects.filter(game=game_id)

    return render(request, 'game-detail.html', {
        'page': 'page-modify-game',
        'menu_data': get_menus_data(request.user.id),
        'game': game,
        'game_form': game_form,
        'notes': notes,
    })


@login_required
def delete_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    # Permission check
    if game.user.id != request.user.id:
        return HttpResponseForbidden('Don\'t be sneaky, you don\'t have permission over this game')

    game.delete()
    messages.success(request, 'The game was successfully deleted')
    return HttpResponseRedirect('/')


# AJAX CONTROLLERS
# ---------------------

@login_required
def finish_game_ajax(request, game_id):
    if not settings.DEBUG and not request.is_ajax():
        return HttpResponseForbidden('Only ajax requests')

    game = get_object_or_404(Game, id=game_id)

    # Permission check
    if game.user.id != request.user.id:
        return HttpResponseForbidden('Don\'t be sneaky, you don\'t have permission over this game')

    if game.stopped_playing_at is not None:
        return HttpResponseForbidden('The game already has a "stopped_playing_at" date.')

    patch = QueryDict(request.body)

    game.stopped_playing_at = date.today()
    game.beaten = bool(patch.get('beaten'))
    game.save()
    return HttpResponse('')  # Give an empty 200


def get_game_ajax(request, game_id):
    if not settings.DEBUG and not request.is_ajax():
        return HttpResponseForbidden('Only ajax requests')

    game = get_object_or_404(Game, id=game_id)

    # Permission check
    if game.user.id != request.user.id and game.id != SHOWCASE_USER_ID:
        return HttpResponseForbidden('Don\'t be sneaky, you don\'t have permission over this game')

    return render(request, 'ajax/game.html', {'game': game})


@login_required
def add_note_to_game_ajax(request, game_id):
    if not settings.DEBUG and not request.is_ajax():
        return HttpResponseForbidden('Only ajax requests')

    game = get_object_or_404(Game, id=game_id)

    # Permission check
    if game.user.id != request.user.id:
        return HttpResponseForbidden('Don\'t be sneaky, you don\'t have permission over this game')

    # POST ----------------------------------------------
    if request.method == 'POST':
        # Check if the user has permission over the game
        note_form = NoteForm(request.POST)
        if not note_form.is_valid():
            return HttpResponse(status=400)

        note = note_form.save(commit=False)
        note.game = game
        note.save()

    return JsonResponse(model_to_dict(note))


@login_required
def scrap_metacritic_ajax(request):
    if not settings.DEBUG and not request.is_ajax():
        return HttpResponseForbidden('Only ajax requests')

    scrap_metacritic_form = ScrapMetacriticForm(request.GET)

    if not scrap_metacritic_form.is_valid():
        return HttpResponse(status=400)

    formData = scrap_metacritic_form.cleaned_data
    scrap_metacritic = metacritic_scrapper(formData['metacritic_url'])

    return JsonResponse(scrap_metacritic)


@login_required
def scrap_hltb_ajax(request):
    if not settings.DEBUG and not request.is_ajax():
        return HttpResponseForbidden('Only ajax requests')

    scrap_hltb_form = ScrapHltbForm(request.GET)

    if not scrap_hltb_form.is_valid():
        return HttpResponse(status=400)

    formData = scrap_hltb_form.cleaned_data
    scrap_hltb = hltb_scrapper(formData['hltb_url'])

    return JsonResponse(scrap_hltb)


class NoteDetailAjaxView(LoginRequiredMixin, View):
    def put(self, request, game_id, note_id):
        note = get_object_or_404(Note, id=note_id)
        game = Game.objects.get(id=note.game.id)

        # Permission check
        if game.user.id != request.user.id:
            return HttpResponseForbidden('Don\'t be sneaky, you don\'t have permission over this note')

        note_form = NoteForm(QueryDict(request.body), instance=note)
        if not note_form.is_valid():
            return HttpResponse(status=400)

        note.save()
        return JsonResponse(model_to_dict(note))

    def delete(self, request, game_id, note_id):
        note = get_object_or_404(Note, id=note_id)
        game = Game.objects.get(id=note.game.id)

        # Permission check
        if game.user.id != request.user.id:
            return HttpResponseForbidden('Don\'t be sneaky, you don\'t have permission over this note')

        note.delete()
        return HttpResponse(status=204)

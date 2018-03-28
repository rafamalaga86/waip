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
from django.db.models import Q
from django.forms.models import model_to_dict
from django.http import QueryDict, HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.shortcuts import HttpResponse, get_object_or_404, render
from django.utils.translation import gettext as _
from django.views import View
from games.utils import metacritic_scrapper, hltb_scrapper, get_menus_data, ScrapRequestException, get_games_order
from urllib.parse import urlencode
import logging


logger = logging.getLogger(__name__)

SHOWCASE_USER_ID = 1


def list_user_games(request):
    user = request.user if request.user.is_authenticated() else User.objects.get(id=SHOWCASE_USER_ID)

    # Get GET query string variables
    year = request.GET.get('year')
    beaten = (request.GET.get('beaten') == '1') if year else False

    filters = {'user_id': user.id}
    if year:
        filters['stopped_playing_at__year'] = year
        filters['beaten'] = beaten
    else:
        filters['stopped_playing_at'] = None

    games = Game.objects.filter(**filters).order_by(*get_games_order(year))

    for game in games:
        game.notes = Note.objects.filter(game_id=game.id).order_by('created_at')

    return render(request, 'game-grid.html', {
        'page': 'page-list-games',
        'menu_data': get_menus_data(user.id),
        'year': year,
        'beaten': beaten,
        'games': games,
    })


@login_required
def search_games(request):
    keyword = request.GET.get('keyword')
    games = None
    if keyword:
        games = Game.objects.filter(Q(name__icontains=keyword) | Q(synopsis__icontains=keyword))
        games = games.filter(user_id=request.user.id)

    return render(request, 'game-grid.html', {
        'page': 'page-search-games',
        'menu_data': get_menus_data(request.user.id),
        'show_status': True,
        'keyword': keyword,
        'games': games,
    })


@login_required
def add_game(request):
    # POST ----------------------------------------------
    if request.method == 'POST':
        game_form = GameForm(request.POST, user_id=request.user.id)
        if game_form.is_valid():
            game = game_form.save(commit=False)
            game.user = request.user
            game.save()

            if game.stopped_playing_at:
                year = str(game.stopped_playing_at.year)
                query_string = '?' + urlencode({
                    'year': year,
                    'beaten': '1' if game.beaten else '0',
                })
                message = _('%(beaten)s at %(year)s  - Successfully added') % {
                    'year': year,
                    'beaten': 'Beaten' if game.beaten else 'Tried',
                }
            else:
                query_string = ''
                message = _('Currently playing game successfully added')

            messages.success(request, message)
            return HttpResponseRedirect('/' + query_string)

    # GET -----------------------------------------------
    else:
        game_form = GameForm()

    # SHARED --------------------------------------------
    trigger_intro = not request.session.get('intro_triggered', False) \
        and Game.objects.filter(user_id=request.user.id).count() == 0
    request.session['intro_triggered'] = True

    context = {
        'page': 'page-add-game',
        'menu_data': get_menus_data(request.user.id),
        'game_form': game_form,
        'trigger_intro': trigger_intro
    }
    return render(request, 'new-game.html', context)


@login_required
def modify_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    # Permission check
    if game.user.id != request.user.id:
        return HttpResponseForbidden(_('Don\'t be sneaky, you don\'t have permission over this game'))

    # POST ----------------------------------------------
    if request.method == 'POST':
        game_form = GameForm(request.POST, instance=game, user_id=request.user.id)
        if game_form.is_valid():
            game.save()
            messages.success(request, _('The game was successfully updated'))
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
        return HttpResponseForbidden(_('Don\'t be sneaky, you don\'t have permission over this game'))

    game.delete()
    messages.success(request, _('The game was successfully deleted'))
    return HttpResponseRedirect('/')


@login_required
def list_all(request):
    games = Game.objects.all().order_by('-created_at')

    for game in games:
        game.notes = Note.objects.filter(game_id=game.id).order_by('created_at')

    return render(request, 'game-grid.html', {
        'page': 'page-list-games',
        'menu_data': get_menus_data(request.user.id),
        'games': games,
    })


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
        return HttpResponseForbidden('The game already has a "stopped_playing_at" date')

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
        return HttpResponse(_(scrap_metacritic_form['metacritic_url'].errors.as_text()), status=400)

    formData = scrap_metacritic_form.cleaned_data

    try:
        scrap_metacritic = metacritic_scrapper(formData['metacritic_url'])
    except ScrapRequestException as error:
        return HttpResponse(str(error), status=400)

    return JsonResponse(scrap_metacritic)


@login_required
def scrap_hltb_ajax(request):
    if not settings.DEBUG and not request.is_ajax():
        return HttpResponseForbidden('Only ajax requests')

    scrap_hltb_form = ScrapHltbForm(request.GET)

    if not scrap_hltb_form.is_valid():
        return HttpResponse(_(scrap_hltb_form['hltb_url'].errors.as_text()), status=400)

    formData = scrap_hltb_form.cleaned_data

    try:
        scrap_hltb = hltb_scrapper(formData['hltb_url'])
    except ScrapRequestException as error:
        return HttpResponse(str(error), status=400)

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

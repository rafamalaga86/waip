from django import forms
from .models import Game, Note
from django.contrib.auth.models import User


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = [
            'name',
            'coverUrl',
            'hltbLength',
            'synopsis',
            'releaseDate',
            'developer',
            'genres',
            'metacriticScore',
            'startedAt',
            'beaten',
            'stopped_playing_at',
        ]
        exclude = ['user']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
        ]


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['text']
        exclude = ['game']


class ScrapMetacriticForm(forms.Form):
    metacritic_url = forms.URLField(required=True)


class ScrapHltbForm(forms.Form):
    hltb_url = forms.URLField(required=True)

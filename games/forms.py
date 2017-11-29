from django import forms
from .models import Game, Note


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
            'finishedAt',
        ]
        exclude = ['user']


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['text']
        exclude = ['game']


class ScrapMetacriticForm(forms.Form):
    metacritic_url = forms.URLField(required=True)


class ScrapHltbForm(forms.Form):
    hltb_url = forms.URLField(required=True)

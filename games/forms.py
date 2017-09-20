from django import forms
from .models import Game


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


class ScrapMetacriticForm(forms.Form):
    metacritic_url = forms.URLField(required=True)


class ScrapHltbForm(forms.Form):
    hltb_url = forms.URLField(required=True)

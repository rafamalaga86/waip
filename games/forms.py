from django import forms
from .models import Game


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = '__all__'


class ScrapGameForm(forms.Form):
    metacriticUrl = forms.URLField(label='Metacritic URL', required=True)
    hltbUrl = forms.URLField(label='HowLongToBeat URL', required=True)

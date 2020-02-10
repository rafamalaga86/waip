from .models import Game, Note, Played
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import re


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = [
            'name',
            'order',
            'cover_url',
            'hltb_length',
            'synopsis',
            'release_date',
            'developer',
            'genres',
            'metacritic_score',
        ]
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id', None)
        super(GameForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        if Game.objects.exclude(id=self.instance.id).filter(user=self.user_id,
                                                            name=self.cleaned_data.get('name')).count():
            raise ValidationError(_('You already have a game with this name'))
        return self.cleaned_data.get('name')

    def clean_cover_url(self):
        if self.cleaned_data.get('cover_url').find('?') != -1:
            raise ValidationError(_('The URL should not include query string'))
        return self.cleaned_data.get('cover_url')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = []


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['text']
        exclude = ['game']


class PlayedForm(forms.ModelForm):
    class Meta:
        model = Played
        fields = ['stopped_playing_at', 'beaten']
        exclude = ['game']

    def __init__(self, *args, **kwargs):
        self.game_id = kwargs.pop('game_id', None)
        super(PlayedForm, self).__init__(*args, **kwargs)

    def clean_stopped_playing_at(self):
        if Played.objects.exclude(id=self.instance.id) \
            .filter(game=self.game_id, stopped_playing_at__isnull=True) \
                .count() and self.cleaned_data.get('stopped_playing_at') is None:

            raise ValidationError(_('You already have a Played of this game in Currently Playing Games'))
        return self.cleaned_data.get('stopped_playing_at')

    def clean(self):
        if self.cleaned_data.get('beaten') and not self.cleaned_data.get('stopped_playing_at'):
            raise ValidationError(_('If you mark game as beaten, you should put a Finish Date ' +
                                    '(even when is not an accurate date, we want to allocate it to a year)'))


class ScrapMetacriticForm(forms.Form):
    metacritic_url = forms.URLField(required=True)

    def clean_metacritic_url(self):
        url = self.cleaned_data.get('metacritic_url')
        if not re.match("^https?:\/\/(www.)?metacritic\.com", url):
            raise ValidationError(_('This is not an URL of Metacritic'))
        return url


class ScrapHltbForm(forms.Form):
    hltb_url = forms.URLField(required=True)

    def clean_hltb_url(self):
        url = self.cleaned_data.get('hltb_url')
        if not re.match("^https?:\/\/(www.)?howlongtobeat\.com", url):
            raise ValidationError(_('This is not an URL of HowLongToBeat'))
        return url

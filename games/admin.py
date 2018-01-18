# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Game, Note
from django.contrib import admin

# Register your models here.


@admin.register(Game)
class AdminGames(admin.ModelAdmin):
    list_display = ('name', 'user', 'startedAt', 'stopped_playing_at', 'id')


admin.site.register(Note)

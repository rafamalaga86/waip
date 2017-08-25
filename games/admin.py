# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Game
from django.contrib import admin

# Register your models here.
# admin.site.register(Game)


@admin.register(Game)
class AdminGames(admin.ModelAdmin):
    list_display = ('name', 'startedAt', 'finishedAt', 'id')
    # list_filter = ('name', 'id')

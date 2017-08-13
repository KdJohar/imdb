# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Movie, Director, Genre


# Register your models here.

class MovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'popularity', 'imdb_score',)
    list_filter = ['is_active', ]


admin.site.register(Movie, MovieAdmin)
admin.site.register(Director)
admin.site.register(Genre)

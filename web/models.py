# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.

class Director(models.Model):
    name = models.CharField(unique=True, max_length=255)

    def __unicode__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(unique=True, max_length=255)

    def __unicode__(self):
        return self.name


class Movie(models.Model):
    name = models.CharField(db_index=True, unique=True, max_length=255)
    director = models.ForeignKey(Director)
    genre = models.ManyToManyField(Genre)
    imdb_score = models.DecimalField(max_digits=4, decimal_places=2)
    popularity = models.DecimalField(max_digits=4, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255)
    modified_by = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

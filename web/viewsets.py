import django_filters
from django.contrib.auth.models import User
from django.db import models
from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Movie, Director, Genre
from .serializers import MovieSerializer, DirectorSerializer, GenreSerializer, UserSerializer


class CustomRangeFilter(django_filters.FilterSet):
    popularity = django_filters.RangeFilter()
    imdb_score = django_filters.RangeFilter()

    class Meta:
        model = Movie
        fields = ['popularity', 'imdb_score', 'director__name', 'genre__name']

        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }


class MovieViewset(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    serializer_class = MovieSerializer
    search_fields = ('name',)
    ordering_fields = ('popularity', 'imdb_score')
    filter_class = CustomRangeFilter
    filter_fields = ('director__name', 'genre__name',)

    def get_queryset(self):
        queryset = Movie.objects.filter(is_active=True)
        """ Perform necessary eager loading of data. """
        # Set up eager loading to avoid N+1 selects
        # select_related for "to-one" relationships
        queryset = queryset.select_related('director', )
        # prefetch_related for "to-many" relationships
        queryset = queryset.prefetch_related('genre', )

        return queryset

    def destroy(self, request, pk=None):
        is_deleted = Movie.objects.filter(pk=pk).update(is_active=False)
        if is_deleted == 1:
            return Response({"message": "Movie Deleted", "data": request.data, "result": True})
        else:
            return Response({"message": "Error in Deleting Movie", "data": request.data, "result": False})


class DirectorViewset(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet):
    serializer_class = DirectorSerializer
    search_fields = ('name',)
    queryset = Director.objects.all()


class GenreViewset(DirectorViewset):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class UserViewset(mixins.CreateModelMixin, GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    search_fields = ()

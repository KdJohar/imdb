from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Movie, Director, Genre


class UserSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=100, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'is_staff', 'token')

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.token = Token.objects.create(user=user)
        return user


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ('id', 'name',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name',)


class MovieSerializer(serializers.ModelSerializer):
    director = DirectorSerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        model = Movie
        fields = ('id', 'name', 'director', 'genre', 'imdb_score', 'popularity',)

    def create(self, validated_data):
        genre_data = validated_data.pop('genre')
        director_data = validated_data.pop('director')
        validated_data['director'], created = Director.objects.get_or_create(name=director_data['name'])
        movie_obj = Movie.objects.create(**validated_data)
        for obj in genre_data:
            g, cre = Genre.objects.get_or_create(name=obj['name'])
            movie_obj.genre.add(g)
        return movie_obj

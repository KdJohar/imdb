from django.contrib.auth import authenticate
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Movie, Director, Genre


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(max_length=100, read_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                # From Django 1.10 onwards the `authenticate` call simply
                # returns `None` for is_active=False users.
                # (Assuming the default `ModelBackend` authentication backend.)
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg, code='authorization')
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        user = validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        validated_data['token'] = token
        return validated_data


class UserSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=100, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'is_staff', 'token')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.token = Token.objects.create(user=user)
        permissions = Permission.objects.filter(content_type__model__in=['genre', 'movie', 'director'])
        for perm in permissions:
            user.user_permissions.add(perm)
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

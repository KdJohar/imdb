"""imdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from web import viewsets

router = DefaultRouter()

router.register(r'movies', viewsets.MovieViewset, 'Movie')
router.register(r'genre', viewsets.GenreViewset, 'Genres')
router.register(r'director', viewsets.DirectorViewset, 'Directors')
router.register(r'auth/register', viewsets.UserViewset, 'User Registration')
router.register(r'auth/login', viewsets.UserLoginViewset, 'User Login')

urlpatterns = [
    url(r'^api/v1/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^login/', include('rest_framework.urls', namespace='rest_framework'))
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      url(r'^__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns

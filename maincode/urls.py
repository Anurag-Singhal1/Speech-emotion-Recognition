from django.contrib import admin
from django.http.response import HttpResponse
from django.urls import path
from maincode import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('teams', views.teams, name='teams'),
    path('developers', views.dev, name='dev')
]
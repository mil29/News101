from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('news-feed/', views.news_feed, name='news_feed'),
]
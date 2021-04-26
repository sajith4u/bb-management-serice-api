"""bbservice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from . import views
from django.http import request

urlpatterns = [
    path('player/<int:player_id>/', views.player_details, name='player_details'),
    path('player/', views.player, name='player'),
    path('team/<int:team_id>/', views.team_details, name='team_details'),
    path('team/<int:team_id>/player', views.best_players, name='best_players'),
    path('team/', views.team, name='team'),
    path('game/', views.game, name='game'),
    path('game/<int:game_id>', views.game_details, name='game_details'),
]

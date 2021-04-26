from django.shortcuts import render
from rest_framework import viewsets
from .models import Player, Team, Player_Stat, Team_Stat
from .serializers import PlayerSerializer, PlayerStatSerializer, TeamSerializer, TeamStatSerializer
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg

''' Get All Players'''


@csrf_exempt
def player(request):
    if request.method == 'GET':
        players = Player.objects.all()
        plyer_serializer = PlayerSerializer(players, many=True)
        return JsonResponse(plyer_serializer.data, safe=False)


@csrf_exempt
def player_details(request, player_id=None):
    if request.method == 'GET':
        player = Player.objects.filter(user_id=player_id).first()
        player_serializer = PlayerSerializer(player)
        player_stat = Player_Stat.objects.filter(player=player.id).all()
        player_stat_serializer = PlayerStatSerializer(player_stat, many=True)
        response = {
            'player': player_serializer.data,
            'stats': player_stat_serializer.data,
            'score_avg': player_stat.aggregate(Avg('score')),
        }
        return JsonResponse(response, safe=False)


@csrf_exempt
def team(request):
    if request.method == 'GET':
        teams = Team.objects.all()
        team_serializer = TeamSerializer(teams, many=True)
        return JsonResponse(team_serializer.data, safe=False)


@csrf_exempt
def team_details(request, team_id=None):
    if request.method == 'GET':
        team = Team.objects.filter(id=team_id).first()
        team_serializer = TeamSerializer(team)
        team_stat = Team_Stat.objects.filter(team_id=team_id).all()
        team_stat_serializer = TeamStatSerializer(team_stat, many=True)

        response = {
            'team': team_serializer.data,
            'games': team_stat_serializer.data
        }
        return JsonResponse(response, safe=False)

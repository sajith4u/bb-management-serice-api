from .models import Player, Team, Player_Stat, Team_Stat, Game
from .serializers import PlayerSerializer, PlayerStatSerializer, TeamSerializer, TeamStatSerializer, GameSerializer, \
    PlayerSummarySerializer
from django.http import JsonResponse
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


''' Get the 90th percentile players In Team '''


@csrf_exempt
def best_players(request, team_id=None):
    if request.method == 'GET':
        team_players = Player.objects.filter(team_id=team_id).all()
        all_stats = []
        for player in team_players:
            player_stat = Player_Stat.objects.filter(player_id=player.id).all()
            player_stat_serializer = PlayerSummarySerializer(player_stat, many=True)
            all_stats = all_stats + player_stat_serializer.data
        all_stats.sort(key=sort_by_score)

        ''' Get the 90th percentile player Margin'''
        player_margin_index = int(round(.9 * (len(all_stats))))
        return JsonResponse(all_stats[player_margin_index:], safe=False)


def sort_by_score(stat):
    return stat.get('score')


@csrf_exempt
def team_details(request, team_id=None):
    if request.method == 'GET':
        team = Team.objects.filter(id=team_id).first()
        team_serializer = TeamSerializer(team)
        team_stat = Team_Stat.objects.filter(team_id=team_id).all()
        team_stat_serializer = TeamStatSerializer(team_stat, many=True)
        team_players = Player.objects.filter(team_id=team_id).all()
        player_serializer = PlayerSerializer(team_players, many=True)

        response = {
            'team': team_serializer.data,
            'team_avg': team_stat.aggregate(Avg('score')),
            'games': team_stat_serializer.data,
            'players': player_serializer.data
        }
        return JsonResponse(response, safe=False)


@csrf_exempt
def game(request):
    if request.method == 'GET':
        games = Game.objects.all()
        game_serializer = GameSerializer(games, many=True)
        return JsonResponse(game_serializer.data, safe=False)


@csrf_exempt
def game_details(request, game_id=None):
    if request.method == 'GET':
        game = Game.objects.filter(id=game_id).first()
        game_serializer = GameSerializer(game)
        player_stat = Player_Stat.objects.filter(game=game.id).all()
        player_stat_serializer = PlayerSummarySerializer(player_stat, many=True)
        response = {
            'game': game_serializer.data,
            'players': player_stat_serializer.data,
        }
        return JsonResponse(response, safe=False)

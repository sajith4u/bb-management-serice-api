from rest_framework import serializers
from .models import Player, Team, Player_Stat, Game, Team_Stat
from django.contrib.auth.models import User


class PlayerSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    id = serializers.CharField(source='user.id')
    team = serializers.CharField()

    class Meta:
        model = Player
        fields = ('id', 'user', 'team', 'height')


class TeamSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Team
        fields = ('name', 'id')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username')


class GameSerializer(serializers.ModelSerializer):
    host_name = serializers.CharField(source='host.name')
    guest_name = serializers.CharField(source='guest.name')
    winner_name = serializers.CharField(source='winner.name')
    class Meta:
        model = Game
        fields = ('host_name', 'guest_name', 'host_score', 'guest_score', 'winner_name', 'round')


class TeamStatSerializer(serializers.ModelSerializer):
    team = serializers.CharField()
    game = serializers.CharField()
    game_id = serializers.CharField(source='game.id')

    class Meta:
        model = Team_Stat
        fields = ('team', 'game', 'score', 'game_id')


class PlayerStatSerializer(serializers.ModelSerializer):
    game = serializers.CharField()
    name = serializers.CharField(source='player.user.username')

    class Meta:
        model = Player_Stat
        fields = ('name', 'game', 'score')

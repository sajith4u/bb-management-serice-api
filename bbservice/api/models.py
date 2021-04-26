from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


class Team(models.Model):
    name = models.TextField(max_length=50)

    def __str__(self):
        return str(self.name)


class Player(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    height = models.IntegerField(null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return 'Name : %s , Height : %s' % (self.user.first_name, self.height)


class Game(models.Model):
    QF = 'QF'
    SF = 'SF'
    FI = 'FI'
    WI = 'WI'

    ROUNDS = [
        (QF, 'Quarter Final'),
        (SF, 'Semi Final'),
        (FI, 'Final'),
        (WI, 'Winner')
    ]

    host = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='host')
    guest = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='guest')
    host_score = models.IntegerField()
    guest_score = models.IntegerField()
    winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='winner')
    date = models.DateField(verbose_name='game_date', null=True)
    round = models.CharField(
        max_length=2,
        choices=ROUNDS,
        default=QF,
        verbose_name='round type'
    )

    def __str__(self):
        return 'Game # Host : %s, Guest : %s, Round : %s' % (self.host.name, self.guest.name, self.round)


class Player_Stat(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True)
    score = models.IntegerField(null=True)

    def __str__(self):
        return 'Player  : %s, Game : %s, Score : %s' % (self.player.user.first_name, self.game.round, self.score)


class Coach(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return 'Name : %s %s' % (self.user.first_name, self.user.last_name)


class UserRole(models.Model):
    COACH = 'C'
    PLAYER = 'P'
    ADMIN = 'A'

    ROLE_TYPES = [
        (COACH, 'Coach'),
        (PLAYER, 'Player'),
        (ADMIN, 'Admin'),
    ]
    type = models.CharField(
        max_length=2,
        choices=ROLE_TYPES,
        default=PLAYER,
        verbose_name='type of role'
    )

    def __str__(self):
        return str(self.type)


class RoleMappings(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    role = models.ForeignKey(UserRole, on_delete=models.CASCADE)
    is_logged_in = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Team_Stat(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game')
    score = models.IntegerField()

    def __str__(self):
        return 'Team Name : %s , Game : %s , Score :%s ' % (self.team.name, self.game.round, self.score)


class User_Login_Stat(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    login_time = models.DateTimeField(verbose_name='login date time', default=timezone.now)
    logout_time = models.DateTimeField(verbose_name='logout date time')

    def __str__(self):
        return str(self.login_time)

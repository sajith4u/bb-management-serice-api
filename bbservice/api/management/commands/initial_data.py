from django.core.management.base import BaseCommand, CommandError
from api.models import Team, UserRole, RoleMappings, Player, Coach, Game, Team_Stat, Player_Stat
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
import random, string


class Command(BaseCommand):
    help = 'Populate data for BMS'

    '''' Add Teams to System '''

    def add_teams(self):
        team_names = ["TEAM 1", "TEAM 2", "TEAM 3", "TEAM 4", "TEAM 5",
                      "TEAM 6", "TEAM 7", "TEAM 8", "TEAM 9", "TEAM 10", "TEAM 11", "TEAM 12", "TEAM 13", "TEAM 14",
                      "TEAM 15", "TEAM 16"]
        for t in range(16):
            try:
                team = Team(name=team_names[t])
            except ObjectDoesNotExist:
                raise CommandError('Team Model Does not exists')
            team.save()
            self.stdout.write(
                self.style.SUCCESS('Successfully inserted Team : "%s" "' % (team.name)))

    '''' Add User Roles '''

    def add_user_roles(self):
        types = ['C', 'P', 'A']
        for type in range(len(types)):
            try:
                role = UserRole(type=types[type])
            except ObjectDoesNotExist:
                raise CommandError('Role Model Does not exists')
            role.save()
            self.stdout.write(self.style.SUCCESS('Successfully inserted data for User Role "%s"' % role.type))

    '''' Add New Auth Users '''

    def add_auth_users(self):
        for type in range(177):
            username = self.get_random_name(10)
            email = username + "@gmail.com"
            password = self.get_random_name(8)
            first_name = self.get_random_name(6)
            last_name = self.get_random_name(6)
            try:
                user = User.objects.create_user(username=username, email=email, password=password,
                                                first_name=first_name, last_name=last_name)
            except ObjectDoesNotExist:
                raise CommandError('User Model Does not exits')
            user.save()
            self.stdout.write(self.style.SUCCESS('User Created : "%s"' % user.username))

    ''' Generate Random String for Length'''

    def get_random_name(self, length):
        return ''.join(
            random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length))

    ''' Add All Users Mappings [players 160, coach 16, admin 1]'''

    def add_user_role_mappings(self):
        users = User.objects.all()
        player = UserRole.objects.filter(type='P').first()
        coach = UserRole.objects.filter(type='C').first()
        admin = UserRole.objects.filter(type='A').first()

        ''' Add All Players (16*10)'''
        for user in users[:160]:
            try:
                role_mappings = RoleMappings(user_id=user.id, role_id=player.id,
                                             is_logged_in=bool(random.getrandbits(1)))
            except ObjectDoesNotExist:
                raise CommandError('Role Model Does not exists')
            role_mappings.save()
            self.stdout.write(self.style.SUCCESS('Add Player Role Mappings  "%s", User "%s" ' % (player.type, user.username)))

        ''' Add All Coaches (1*16)'''
        for user in users[160:176]:
            try:
                role_mappings = RoleMappings(user_id=user.id, role_id=coach.id,
                                             is_logged_in=bool(random.getrandbits(1)))
            except ObjectDoesNotExist:
                raise CommandError('Role Model Does not exists')
            role_mappings.save()
            self.stdout.write(self.style.SUCCESS('Add Coach Role Mappings "%s, User "%s "' % (coach.type,user.username)))

        ''' Add Super Admin (1)'''
        try:
            role_mappings = RoleMappings(user_id=users[176].id, role_id=admin.id,
                                         is_logged_in=bool(random.getrandbits(1)))
        except ObjectDoesNotExist:
            raise CommandError('Role Model Does not exists')
        role_mappings.save()
        self.stdout.write(self.style.SUCCESS('Add Admin Role Mappings "%s", User "%s"' % (admin.type,user.username)))

    ''' Add Player to Teams'''

    def add_players(self):
        teams = Team.objects.all()
        role = UserRole.objects.filter(type='P').first()
        user_mappings = RoleMappings.objects.filter(role_id=role.id)
        user_index = 0;
        for team in teams:
            for team_size in range(10):
                try:
                    player = Player(team_id=team.id, user_id=user_mappings[user_index].user.id,
                                    height=random.randint(120, 170))
                except ObjectDoesNotExist:
                    raise CommandError('User Add Failed')
                player.save()
                self.stdout.write(self.style.SUCCESS('Successfully add Player  "%s"  to team "%s"' % (
                    user_mappings[user_index].user.first_name, team.name)))
                user_index += 1

    ''' Add Coach to Teams'''

    def add_coaches(self):
        teams = Team.objects.all()
        role = UserRole.objects.filter(type='C').first()
        coach_mappings = RoleMappings.objects.filter(role_id=role.id)
        for team_size in range(len(teams)):
            try:
                coach = Coach(team_id=teams[team_size].id, user_id=coach_mappings[team_size].user.id)
            except ObjectDoesNotExist:
                raise CommandError('Failed to Add Coach')
            coach.save()
            self.stdout.write(self.style.SUCCESS('Successfully add Coach   "%s"  to team "%s"' % (
                coach_mappings[team_size].user.first_name, teams[team_size].name)))

    ''' Add QF Games (assume equal score give first team as winner)'''

    def add_qf_matches(self):
        teams = Team.objects.all()
        team_size = len(teams)
        first_half = teams[:team_size // 2]
        second_half = teams[team_size // 2:]
        for team in range(len(teams) // 2):
            first_team_score = random.randint(0, 10)
            second_team_score = random.randint(0, 10)
            win_team = first_half[team] if first_team_score >= second_team_score else second_half[team]

            try:
                game = Game(host_id=first_half[team].id, guest_id=second_half[team].id,
                            host_score=first_team_score, guest_score=second_team_score, winner_id=win_team.id,
                            round="QF")
            except ObjectDoesNotExist:
                raise CommandError('Failed to Add QF Games')
            game.save()
            self.stdout.write(
                self.style.SUCCESS(
                    'Successfully add QF Game   First Team : "%s"  Second Team :  "%s" : Score : "%s:%s" : Winner : "%s" ' % (
                        first_half[team].name, second_half[team].name, first_team_score, second_team_score,
                        win_team.name)))

    ''' Add SF Games'''

    def add_sf_matches(self):
        ''' Select QF win Teams List '''
        qf_teams = Team.objects.filter(id__in=Game.objects.filter(round='QF').values_list('winner', flat=True))
        team_size = len(qf_teams)
        first_half = qf_teams[:team_size // 2]
        second_half = qf_teams[team_size // 2:]
        for team in range(len(qf_teams) // 2):
            first_team_score = random.randint(0, 10)
            second_team_score = random.randint(0, 10)
            win_team = first_half[team] if first_team_score >= second_team_score else second_half[team]

            try:
                game = Game(host_id=first_half[team].id, guest_id=second_half[team].id,
                            host_score=first_team_score, guest_score=second_team_score, winner_id=win_team.id,
                            round="SF")
            except ObjectDoesNotExist:
                raise CommandError('Failed to Add SF Games')
            game.save()
            self.stdout.write(
                self.style.SUCCESS(
                    'Successfully add SF Game   First Team : "%s"  Second Team :  "%s" : Score : "%s:%s" : Winner : "%s" ' % (
                        first_half[team].name, second_half[team].name, first_team_score, second_team_score,
                        win_team.name)))

    ''' Add FI Games'''

    def add_fi_matches(self):
        ''' Select QF win Teams List '''
        sf_teams = Team.objects.filter(id__in=Game.objects.filter(round='SF').values_list('winner', flat=True))
        team_size = len(sf_teams)
        first_half = sf_teams[:team_size // 2]
        second_half = sf_teams[team_size // 2:]
        for team in range(len(sf_teams) // 2):
            first_team_score = random.randint(0, 10)
            second_team_score = random.randint(0, 10)
            win_team = first_half[team] if first_team_score >= second_team_score else second_half[team]

            try:
                game = Game(host_id=first_half[team].id, guest_id=second_half[team].id,
                            host_score=first_team_score, guest_score=second_team_score, winner_id=win_team.id,
                            round="FI")
            except ObjectDoesNotExist:
                raise CommandError('Failed to Add FI Games')
            game.save()
            self.stdout.write(
                self.style.SUCCESS(
                    'Successfully add FI Game   First Team : "%s"  Second Team :  "%s" : Score : "%s:%s" : Winner : "%s" ' % (
                        first_half[team].name, second_half[team].name, first_team_score, second_team_score,
                        win_team.name)))

    ''' Add Winning Game'''

    def add_wi_matches(self):
        ''' Select QF win Teams List '''
        sf_teams = Team.objects.filter(id__in=Game.objects.filter(round='FI').values_list('winner', flat=True))
        team_size = len(sf_teams)
        first_half = sf_teams[:team_size // 2]
        second_half = sf_teams[team_size // 2:]
        for team in range(len(sf_teams) // 2):
            first_team_score = random.randint(0, 10)
            second_team_score = random.randint(0, 10)
            win_team = first_half[team] if first_team_score >= second_team_score else second_half[team]

            try:
                game = Game(host_id=first_half[team].id, guest_id=second_half[team].id,
                            host_score=first_team_score, guest_score=second_team_score, winner_id=win_team.id,
                            round="WI")
            except ObjectDoesNotExist:
                raise CommandError('Failed to Add SF Games')
            game.save()
            self.stdout.write(
                self.style.SUCCESS(
                    'Successfully add Final Game   First Team : "%s"  Second Team :  "%s" : Score : "%s:%s" : Winner : "%s" ' % (
                        first_half[team].name, second_half[team].name, first_team_score, second_team_score,
                        win_team.name)))

    ''' Add Team Stats'''

    def add_team_stats(self):
        teams = Team.objects.all()
        for team in teams:
            scores = Game.objects.filter(Q(host_id=team.id) | Q(guest_id=team.id))
            for team_score in scores:
                team_id = team_score.host_id if team_score.host_id == team.id else team_score.guest_id
                game_score = team_score.host_score if team_score.host_id == team.id else team_score.guest_score

                host_stat = Team_Stat(score=game_score, game_id=team_score.id, team_id=team_id)
                host_stat.save()
                self.stdout.write(self.style.SUCCESS('Team Stats Added  # %s ' % team_score.id))

    ''' Add Team Stats'''

    def add_player_stat(self):
        team_stats = Team_Stat.objects.all()
        for ts in team_stats:
            ''' Assume All the players score runs for match '''
            players = Player.objects.filter(team_id=ts.team_id)
            score = random.randint(0, 10)
            for player in players:
                player_stat = Player_Stat(player_id=player.id, game_id=ts.game.id, score=score);
                player_stat.save()
                self.stdout.write(self.style.SUCCESS(
                    'Player Stats Added for %s , Geme : %s' % (player.user.first_name, player.team.name)))

    ''' Clean All Tables '''

    def clean_database(self):
        Team.objects.all().delete()
        UserRole.objects.all().delete()
        User.objects.all().delete()
        RoleMappings.objects.all().delete()
        Player.objects.all().delete()
        Coach.objects.all().delete(),
        Game.objects.all().delete()
        Player_Stat.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('====== Clean Database Success ========"'))

    def handle(self, *args, **options):

        self.clean_database()
        self.add_teams()
        self.add_user_roles()
        self.add_auth_users()
        self.add_user_role_mappings()
        self.add_players()
        self.add_coaches()
        self.add_qf_matches()
        self.add_sf_matches()
        self.add_fi_matches()
        self.add_wi_matches()
        self.add_team_stats()
        self.add_player_stat()

from django.contrib import admin
from .models import Player,Team, Player_Stat, Game, Coach, Team_Stat, UserRole, RoleMappings

# Register your models here.

admin.site.register(Player)
admin.site.register(Team)
admin.site.register(Player_Stat)
admin.site.register(Game)
admin.site.register(Coach)
admin.site.register(Team_Stat)
admin.site.register(UserRole)
admin.site.register(RoleMappings)

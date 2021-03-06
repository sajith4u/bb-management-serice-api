# Generated by Django 3.2 on 2021-04-24 19:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0013_auto_20210424_1802'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('C', 'Coach'), ('P', 'Player'), ('A', 'Admin')], default='P', max_length=2, verbose_name='type of role')),
            ],
        ),
        migrations.CreateModel(
            name='Team_Stat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game', to='api.game')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team', to='api.team')),
            ],
        ),
        migrations.CreateModel(
            name='RoleMappings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_logged_in', models.BooleanField(default=False)),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.userrole')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

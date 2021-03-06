# Generated by Django 3.2 on 2021-04-25 06:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0014_rolemappings_team_stat_userrole'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Login_Stat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='login date time')),
                ('logout_time', models.DateTimeField(verbose_name='logout date time')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

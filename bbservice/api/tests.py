from django.urls import include, path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework import status
from .models import Player, Team, Player_Stat, Game, Team_Stat


# Create your tests here.

class PlayerTest(APITestCase):
    urlpatterns = [
        path('', include('api.urls')),
    ]

    def test_all_teams(self):
        url = reverse('team')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

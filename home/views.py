# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from games.models import Game
from teams.models import Team

# Create your views here.
# The default home page view.
def home_page(request):

	games = Game.objects.all().values('game_date', 'home_team', 'away_team', 'home_score', 'away_score')
	teams = Team.objects.all()

	return render(request, "home.html", {"games": games, "teams": teams})
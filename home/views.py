# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from games.models import Game, Competition
from teams.models import Team

# Create your views here.
# The default home page view.
def home_page(request):

	results = Game.objects.filter(game_status="Completed")
	competitions = Competition.objects.all()
	teams = Team.objects.all()

	latest_date = results.order_by('-game_date')[0].game_date
	latest_results = Game.objects.filter(game_date=latest_date)\
		.order_by('home_team').values('competition', 'home_team', 'away_team', 'home_score', 'away_score')

	return render(request, "home.html", {"latest_date": latest_date, "latest_results": latest_results,\
		"competitions": competitions, "teams": teams})
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from models import Game, League, Competition, Season
from teams.models import Team

# Create your views here.
# The latest results page view.
def latest_results(request):

	games = Game.objects.all().values('game_date', 'home_team', 'away_team', 'home_score', 'away_score')
	teams = Team.objects.all()

	return render(request, "latest_results.html", {"games": games, "teams": teams})


# Show the league table for the given competition.
def league_tables(request):

	current_season = Season.objects.latest('id')

	leagues = League.objects.all()
	competitions = Competition.objects.filter(season=current_season)

	return render(request, "league_tables.html", {"leagues": leagues, "competitions": competitions, "current_season": current_season})
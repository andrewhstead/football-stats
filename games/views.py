# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from models import Game, League, Competition, Season
from teams.models import Team
from countries.models import Country

# Create your views here.
# The latest results page view.
def latest_results(request):

	games = Game.objects.all().values('game_date', 'home_team', 'away_team', 'home_score', 'away_score')
	teams = Team.objects.all()

	return render(request, "latest_results.html", {"games": games, "teams": teams})


# Show the index of league tables for the current season.
def league_tables(request):

	current_season = Season.objects.latest('id')
	competitions = Competition.objects.filter(season=current_season)

	return render(request, "league_tables.html", {"competitions": competitions, "current_season": current_season})


# Show the league table for the given competition.
def competition_table(request, country, competition, season):

	country = Country.objects.get(abbreviation=country.upper())
	season = Season.objects.get(name=season)

	competition = Competition.objects.get(country_id=country.id, abbreviation=competition.upper(), season_id=season.id)
	teams = [team for team in competition.teams.all()]

	return render(request, "competition_table.html", {"competition": competition, "teams": teams})
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from models import Game, League, Competition, Season, Adjustment
from utils import get_competition, get_details, colour_table
from teams.models import Club, Team
from countries.models import Country
import datetime

# Create your views here.
# The latest results page view.
def latest_results(request):

	games = Game.objects.all().values('game_date', 'home_team', 'away_team', 'home_score', 'away_score')
	teams = Team.objects.all()

	return render(request, "latest_results.html", {"games": games, "teams": teams})


# View for results on a specific day.
def date_results(request, day, month, year):

	game_date = datetime.datetime(year=int(year), month=int(month), day=int(day))
	games = Game.objects.filter(game_date=game_date)\
		.values('competition', 'season', 'home_team', 'away_team', 'home_score', 'away_score')

	teams = Team.objects.all()

	# Empty list to hold the IDs of all competitions in which games were played on the chosen date.
	date_competitions = []

	# Check each game and if its competition is not in the list, add it.
	for game in games:
		if game['competition'] not in date_competitions:
			date_competitions.append(game['competition'])

	# Filter the competitions to include only those where games were played on the chosen date.
	competitions = Competition.objects.filter(id__in=date_competitions)

	return render(request, "date_results.html",\
	 {"game_date": game_date, "games": games, "competitions": competitions, "teams": teams})


# Show the index of league tables for the current season.
def league_tables(request):

	current_season = Season.objects.latest('id')
	competitions = Competition.objects.filter(season=current_season)

	return render(request, "league_tables.html", {"competitions": competitions, "current_season": current_season})


# Show the index of available seasons.
def season_index(request):

	seasons = Season.objects.all()

	return render(request, "seasons.html", {"seasons": seasons})


# Show the league table for the given competition.
def competition_details(request, country, competition, season):

	# Get the competition from the supplied parameters using an external function.
	competition = get_competition(country, competition, season)
	# Get the teams involved in this competition.
	teams = competition.teams.all().values('id', 'club', 'short_name', 'abbreviation')

	# Set the tie-breaking method to be shown in the league table.
	# If the first tie-breaker is Goal Average, this will be shown. Otherwise Goal Difference is shown.
	if competition.tie_breaker_1 == "Goal Average":
		table_tie_breaker = "GA"
	else:
		table_tie_breaker = "GD"

	# Construct the zones to be shaded in the league table using an external function.
	table_zones = colour_table(teams, competition)

	# Construct the team records for the league table using an external function.
	details = get_details(competition)

	return render(request, "competition_details.html",\
		{"competition": competition,\
		 "teams": details[0], "games": details[1],\
		 "league_table": details[2], "adjustments": details[3],\
		 "table_tie_breaker": table_tie_breaker, "table_zones": table_zones})
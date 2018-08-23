# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from models import Club, Team
from games.models import League, Game, Season
from countries.models import Country
from django.db.models import Q

# Create your views here.
# The main club index.
def club_index(request):

	countries = Country.objects.all().order_by('full_name')
	leagues = League.objects.all().order_by('tier')
	clubs = Club.objects.all().order_by('full_name').values('full_name', 'current_league')

	# Generate a list of clubs currently in each league.
	for league in leagues:
		league.current_clubs = []
		for club in clubs:
			if club['current_league'] == league.id:
				league.current_clubs.append(club)

	return render(request, "clubs.html", {"clubs": clubs, "leagues": leagues, "countries": countries})


# Show the results of a given team for a given season.
def team_season(request, team, season):

	# Find the club and current team name.
	club = Club.objects.get(abbreviation=team.upper())
	team = Team.objects.get(club=club)

	# Full list of teams to get names of opponents.
	teams = Team.objects.all()

	season = Season.objects.get(name=season)

	# Empty list to hold the team's games for the season
	team_games = []

	games = Game.objects.filter(Q(season=season) & (Q(home_team=team) | Q(away_team=team)))\
		.values('game_date', 'home_team', 'away_team', 'home_score', 'away_score')\
		.order_by('game_date', 'game_time')

	# For each game in the season:
	for game in games:
		# If the team was at home, allocate the home team's result to them and set the away team as their opponent.
		if game['home_team'] == team.id:
			details = {"venue": "H", "team": game['home_team'], "opponent": game['away_team'],
					"goals_for": game['home_score'], "goals_against": game['away_score'],
					"date": game['game_date']}
		# If the chosen team was away, allocate the away team's result to them and set the home team as their opponent.
		else:
			details = {"venue": "A", "team": game['away_team'], "opponent": game['home_team'],
					"goals_for": game['away_score'], "goals_against": game['home_score'],
					"date": game['game_date']}
		team_games.append(details)

	return render(request, "team_season.html", {"team": team, "season": season, "team_games": team_games, "teams": teams})
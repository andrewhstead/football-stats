# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from models import Game, League, Competition, Season, Adjustment
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

	# Empty list to contain the league table.
	league_table = []

	# Define the country and season and then use these to select the competition.
	country = Country.objects.get(abbreviation=country.upper())
	season = Season.objects.get(name=season)
	competition = Competition.objects.get(country_id=country.id, abbreviation=competition.upper(), season_id=season.id)
	adjustments = Adjustment.objects.filter(competition=competition)

	# Set the tie-breaking method to be shown in the league table.
	# If the first tie-breaker is Goal Average, this will be shown. Otherwise Goal Difference is shown.
	if competition.tie_breaker_1 == "Goal Average":
		table_tie_breaker = "GA"
	else:
		table_tie_breaker = "GD"

	# Convert the competition's tie-breakers for use in table sorting.
	tie_breaker_1 = competition.tie_breaker_1.lower().replace(" ", "_")
	if competition.tie_breaker_2:
		tie_breaker_2 = competition.tie_breaker_2.lower().replace(" ", "_")	
	if competition.tie_breaker_3:
		tie_breaker_3 = competition.tie_breaker_3.lower().replace(" ", "_")
	if competition.tie_breaker_4:
		tie_breaker_4 = competition.tie_breaker_4.lower().replace(" ", "_")
	if competition.tie_breaker_5:
		tie_breaker_5 = competition.tie_breaker_5.lower().replace(" ", "_")

	# Select the teams and the games for this competition.
	teams = competition.teams.all()
	games = Game.objects.filter(competition=competition)\
	.values('game_date', 'home_team', 'away_team', 'home_score', 'away_score')

	# Construct an dictionary for each team's playing record with all statistics set to 0.
	# Floats are used rather than integers in order to facilitate calculations.
	for team in teams:
		
		team_record = {"name": team.short_name,\
			"games_played": 0.0,\
			"games_won": 0.0, "games_drawn": 0.0, "games_lost": 0.0, "goals_for": 0.0, "goals_against": 0.0,\
			"home_won": 0.0, "home_drawn": 0.0, "home_lost": 0.0, "home_for": 0.0, "home_against": 0.0,\
			"away_won": 0.0, "away_drawn": 0.0, "away_lost": 0.0, "away_for": 0.0, "away_against": 0.0,\
			"goal_average": 0.0, "goal_difference": 0.0, "points": 0.0}

		# Next get the team's completed home games and away games for the current year.
		home_games = [game for game in games if game['home_team'] == team.id]
		away_games = [game for game in games if game['away_team'] == team.id]

		# For each home game, add the game result and score to the team's record.
		for game in home_games:
			team_record["games_played"] += 1
			team_record["goals_for"] += game['home_score']
			team_record["goals_against"] += game['away_score']
			if game['home_score'] > game['away_score']:
				team_record["games_won"] += 1
				team_record["home_won"] += 1
				team_record["points"] += competition.home_win_points
			if game['home_score'] == game['away_score']:
				team_record["games_drawn"] += 1
				team_record["home_drawn"] += 1
				team_record["points"] += competition.home_draw_points
			if game['home_score'] < game['away_score']:
				team_record["games_lost"] += 1
				team_record["home_lost"] += 1
				team_record["points"] += competition.home_loss_points

		# For each away game, add the game result and score to the team's record.
		for game in away_games:
			team_record["games_played"] += 1
			team_record["goals_for"] += game['away_score']
			team_record["goals_against"] += game['home_score']
			if game['home_score'] < game['away_score']:
				team_record["games_won"] += 1
				team_record["away_won"] += 1
				team_record["points"] += competition.away_win_points
			if game['home_score'] == game['away_score']:
				team_record["games_drawn"] += 1
				team_record["away_drawn"] += 1
				team_record["points"] += competition.away_draw_points
			if game['home_score'] > game['away_score']:
				team_record["games_lost"] += 1
				team_record["away_lost"] += 1
				team_record["points"] += competition.away_loss_points

		# Set up the team's goal average and goal difference.
		if team_record["goals_against"] > 0.0:
				team_record["goal_average"] = team_record["goals_for"] / team_record["goals_against"]
		team_record["goal_difference"] = team_record["goals_for"] - team_record["goals_against"]

		# Check whether the team has a points adjustment and if so, apply it to their record.
		for adjustment in adjustments:
			if adjustment.team == team:
				team_record["points"] += adjustment.points
				team_record["name"] += " *"

		# Add the team's updated record to the league table.
		league_table.append(team_record)

	# Sort the league table by all chosen tiebreaking criteria.
	league_table.sort(key=lambda team_record:[team_record["points"], team_record[tie_breaker_1], team_record[tie_breaker_2],\
	 team_record[tie_breaker_3], team_record[tie_breaker_4], team_record[tie_breaker_5]], reverse=True)

	return render(request, "competition_table.html",\
		{"competition": competition, "teams": teams, "league_table": league_table,\
		 "table_tie_breaker": table_tie_breaker, "adjustments": adjustments})
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from models import Game, Adjustment, Season, Competition
from countries.models import Country
from teams.models import Club

# function to create a league table.
def get_competition(country, competition, season):

	# Define the country and season and then use these to select the competition.
	country = Country.objects.get(abbreviation=country.upper())
	season = Season.objects.get(name=season)
	competition = Competition.objects.get(country_id=country.id, abbreviation=competition.upper(), season_id=season.id)

	return competition


# function to create a league table.
def colour_table(teams, competition):

	# Work out a list of all possible positions in the table and construct the zones to be shaded in the table.
	team_total = teams.count()
	positions = range(1, (team_total + 1))

	top_primary = positions[0:competition.top_primary_places]
	top_secondary = positions[competition.top_primary_places:(competition.top_primary_places + competition.top_secondary_places)]
	
	bottom_primary = positions[(team_total - competition.bottom_primary_places):team_total]
	if competition.bottom_primary_places == 0:
		bottom_secondary = positions[-competition.bottom_secondary_places:]
	else:
		bottom_secondary = positions[-(competition.bottom_secondary_places + competition.bottom_primary_places):-competition.bottom_primary_places]

	return {"top_primary": top_primary, "top_secondary": top_secondary,\
		  "bottom_primary": bottom_primary, "bottom_secondary": bottom_secondary}


# function to create a league table.
def get_details(competition):

	# Select the teams and the games for this competition.
	# Clubs are also needed to use club abbreviation in URLs.
	clubs = Club.objects.all().values('id', 'abbreviation')
	teams = competition.teams.all().values('id', 'club', 'short_name', 'abbreviation')
	games = Game.objects.filter(competition=competition)\
		.values('game_date', 'home_team', 'away_team', 'home_score', 'away_score')

	# Select any points adjustments which apply to this competition.
	adjustments = Adjustment.objects.filter(competition=competition)

	# Set up the competition's tie-breakers for use in table sorting.
	# Add the lowest ranking tie-breaker first so that the highest ranking is applied last before points are used.
	tie_breakers = []
	tie_breaker_5 = competition.tie_breaker_5.lower().replace(" ", "_")
	tie_breakers.append(tie_breaker_5)
	tie_breaker_4 = competition.tie_breaker_4.lower().replace(" ", "_")
	tie_breakers.append(tie_breaker_4)
	tie_breaker_3 = competition.tie_breaker_3.lower().replace(" ", "_")
	tie_breakers.append(tie_breaker_3)
	tie_breaker_2 = competition.tie_breaker_2.lower().replace(" ", "_")
	tie_breakers.append(tie_breaker_2)
	tie_breaker_1 = competition.tie_breaker_1.lower().replace(" ", "_")
	tie_breakers.append(tie_breaker_1)

	# Empty list to contain the league table.
	table_records = []
	
	# Construct an dictionary for each team's playing record with all statistics set to 0.
	# Floats are used rather than integers in order to facilitate calculations.
	for team in teams:

		# Work out which club matches the team and use that abbreviation in the team's record for URL construction.
		for club in clubs:
			if club['id'] == team['club']:
				this_club = club
		club_abbreviation = this_club['abbreviation']

		team_record = {"name": team['short_name'], "abbreviation": club_abbreviation,\
			"games_played": 0.0,\
			"games_won": 0.0, "games_drawn": 0.0, "games_lost": 0.0, "goals_for": 0.0, "goals_against": 0.0,\
			"home_won": 0.0, "home_drawn": 0.0, "home_lost": 0.0, "home_for": 0.0, "home_against": 0.0,\
			"away_won": 0.0, "away_drawn": 0.0, "away_lost": 0.0, "away_for": 0.0, "away_against": 0.0,\
			"goal_average": 0.0, "goal_difference": 0.0, "points": 0.0}

		# Next get the team's completed home games and away games for the current year.
		home_games = [game for game in games if game['home_team'] == team['id']]
		away_games = [game for game in games if game['away_team'] == team['id']]

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
			if adjustment.team.short_name == team_record["name"]:
				team_record["points"] += adjustment.points
				team_record["name"] += " *"

		# Add the team's updated record to the league table.
		table_records.append(team_record)

	# Sort the league table by all chosen tiebreaking criteria.
	for tie_breaker in tie_breakers:
		if tie_breaker == "name":
			table_records.sort(key=lambda team_record:team_record[tie_breaker])
		else:
			table_records.sort(key=lambda team_record:team_record[tie_breaker], reverse=True)

	# Finally, sort by points.
	table_records.sort(key=lambda team_record:team_record["points"], reverse=True)


	return (teams, games, table_records, adjustments)
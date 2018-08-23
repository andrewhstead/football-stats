# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from models import Club, Team
from games.models import League
from countries.models import Country

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

	season = season

	return render(request, "team_season.html", {"team": team, "season": season})
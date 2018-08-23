# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from models import Club
from games.models import League
from countries.models import Country

# Create your views here.
# The main club index.
def club_index(request):

	countries = Country.objects.all().order_by('full_name')
	leagues = League.objects.all().order_by('tier')
	clubs = Club.objects.all().order_by('full_name').values('full_name', 'current_league')

	for league in leagues:
		league.current_clubs = []
		for club in clubs:
			if club['current_league'] == league.id:
				league.current_clubs.append(club)

	return render(request, "clubs.html", {"clubs": clubs, "leagues": leagues, "countries": countries})

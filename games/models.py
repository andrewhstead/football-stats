# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from countries.models import Country
from teams.models import Team

# The options for game status which are available in the administration area.
STATUS_OPTIONS = (
    ('Scheduled', "Scheduled"),
    ('Completed', "Completed"),
)

# The options for tie-breakers which can be used in leagues.
TIE_BREAKERS = (
    ('Goal Average', "Goal Average"),
    ('Goal Difference', "Goal Difference"),
    ('Goals Scored', "Goals Scored"),
    ('Games Won', "Games Won"),
    ('Name', "Name"),
)

# Create your models here.

# League model for overall competitions.
class League(models.Model):
	country = models.ForeignKey(Country, related_name='leagues')
	name = models.CharField(max_length=25)
	abbreviation = models.CharField(max_length=3)
	tier = models.IntegerField()

	def __unicode__(self):
		return self.name

# Season model.
class Season(models.Model):
	name = models.CharField(max_length=10)
	end_year = models.IntegerField()

	def __unicode__(self):
		return self.name

# Competition model for individual league seasons.
class Competition(models.Model):
	country = models.ForeignKey(Country, related_name='competitions')
	league = models.ForeignKey(League, related_name='competitions')
	season = models.ForeignKey(Season, related_name='competitions')
	name = models.CharField(max_length=25)
	abbreviation = models.CharField(max_length=3)
	teams = models.ManyToManyField(Team, related_name='teams', blank=True)
	home_win_points = models.IntegerField(default=3)
	away_win_points = models.IntegerField(default=3)
	home_draw_points = models.IntegerField(default=1)
	away_draw_points = models.IntegerField(default=1)
	home_loss_points = models.IntegerField(default=0)
	away_loss_points = models.IntegerField(default=0)
	# Tie breakers default to 'Name' to ensure alphabetical sorting once all other criteria have been applied.
	tie_breaker_1 = models.CharField(max_length=25, choices=TIE_BREAKERS, default="Name")
	tie_breaker_2 = models.CharField(max_length=25, choices=TIE_BREAKERS, default="Name")
	tie_breaker_3 = models.CharField(max_length=25, choices=TIE_BREAKERS, default="Name")
	tie_breaker_4 = models.CharField(max_length=25, choices=TIE_BREAKERS, default="Name")
	tie_breaker_5 = models.CharField(max_length=25, choices=TIE_BREAKERS, default="Name")
	# Places to indicate promotion and relegation issues etc.
	top_primary_places = models.IntegerField(blank=True, null=True)
	top_secondary_places = models.IntegerField(blank=True, null=True)
	bottom_primary_places = models.IntegerField(blank=True, null=True)
	bottom_secondary_places = models.IntegerField(blank=True, null=True)

	def __unicode__(self):
		return unicode(self.name) + ': ' + unicode(self.season)

# Game model for individual matches.
class Game(models.Model):
	competition = models.ForeignKey(Competition, related_name='games')
	game_status = models.CharField(max_length=10, choices=STATUS_OPTIONS, default="Scheduled")
	game_date = models.DateField()
	game_time = models.TimeField(blank=True, null=True)
	home_team = models.ForeignKey(Team, related_name='game_home')
	away_team = models.ForeignKey(Team, related_name='game_away')
	home_score = models.IntegerField(blank=True, null=True)
	away_score = models.IntegerField(blank=True, null=True)

	def __unicode__(self):
		return unicode(self.game_date) + ': ' + unicode(self.home_team) + ' v ' + unicode(self.away_team)

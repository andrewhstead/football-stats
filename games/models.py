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

# Create your models here.

# Competition model to set up leagues.
class Competition(models.Model):
	country = models.ForeignKey(Country, related_name='competitions')
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

# Game model for individual matches.
class Game(models.Model):
	competition = models.ForeignKey(Competition, related_name='results')
	season = models.ForeignKey(Season, related_name='games')
	game_status = models.CharField(max_length=10, choices=STATUS_OPTIONS, default="Scheduled")
	game_date = models.DateField()
	game_time = models.TimeField(blank=True, null=True)
	home_team = models.ForeignKey(Team, related_name='game_home')
	away_team = models.ForeignKey(Team, related_name='game_away')
	home_score = models.IntegerField(blank=True, null=True)
	away_score = models.IntegerField(blank=True, null=True)

	def __unicode__(self):
		return unicode(self.game_date) + ': ' + unicode(self.home_team) + ' v ' + unicode(self.away_team)

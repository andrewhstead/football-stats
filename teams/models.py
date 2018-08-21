# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from countries.models import Country

# Create your models here.

# Club model - a club must have a unique name to identify it throughout the site.
class Club(models.Model):
	full_name = models.CharField(max_length=50, unique=True)
	short_name = models.CharField(max_length=15, unique=True)
	abbreviation = models.CharField(max_length=3, unique=True)
	country = models.ForeignKey(Country, related_name='clubs')

	def __unicode__(self):
		return self.full_name


# Team model - a team is the identity used by a club at any given time.
# It is linked to the club model in order to group different names used by the same club.
class Team(models.Model):
	club = models.ForeignKey(Club, related_name='teams')
	full_name = models.CharField(max_length=50)
	short_name = models.CharField(max_length=15)
	abbreviation = models.CharField(max_length=3)

	def __unicode__(self):
		return self.full_name
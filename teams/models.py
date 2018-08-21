# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.
# The country or continent in which a competition is based.
class Club(models.Model):
	full_name = models.CharField(max_length=50)
	short_name = models.CharField(max_length=15)
	abbreviation = models.CharField(max_length=3)

	def __unicode__(self):
		return self.full_name


# The details of a competition.
class Team(models.Model):
	club = models.ForeignKey(Club, related_name='teams')
	full_name = models.CharField(max_length=50)
	short_name = models.CharField(max_length=15)
	abbreviation = models.CharField(max_length=3)
    	
	def __unicode__(self):
		return self.full_name
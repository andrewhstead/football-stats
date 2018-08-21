# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

# Model to set up continental confederations.
class Continent(models.Model):
	geographic_name = models.CharField(max_length=15)
	official_name = models.CharField(max_length=10)

	def __unicode__(self):
		return self.geographic_name

# Model to set up available counties.
class Country(models.Model):
	full_name = models.CharField(max_length=50)
	short_name = models.CharField(max_length=15)
	abbreviation = models.CharField(max_length=3, unique=True)
	continent = models.ForeignKey(Continent, related_name='countries')

	def __unicode__(self):
		return self.full_name

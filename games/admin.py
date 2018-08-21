# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Competition, Game, League, Season

# Register your models here.
admin.site.register(Competition)
admin.site.register(Game)
admin.site.register(League)
admin.site.register(Season)
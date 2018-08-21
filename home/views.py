# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from games.models import Game

# Create your views here.
# The default home page view.
def home_page(request):

	games = Game.objects.all()

	return render(request, "home.html", {"games": games})
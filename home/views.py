# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
# The default home page view.
def home_page(request):

    return render(request, "home.html")
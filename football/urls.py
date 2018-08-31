"""football URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from games import views as game_views
from home import views as home_views
from teams import views as team_views
from django.views.static import serve
from .settings import MEDIA_ROOT

urlpatterns = [
    url(r'^$', home_views.home_page, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^clubs/$', team_views.club_index, name='club_index'),
    url(r'^clubs/(?P<club>.*)/', team_views.club_overview, name='club_overview'),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    url(r'^tables/$', game_views.league_tables, name='league_tables'),
    url(r'^tables/(?P<country>.*)/(?P<competition>.*)/(?P<season>.*)/$', game_views.competition_details, name='competition_details'),
    url(r'^teams/(?P<team>.*)/(?P<season>.*)/$', team_views.team_season, name='team_season'),
    url(r'^results/$', game_views.latest_results, name='latest_results'),
    url(r'^results/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', game_views.date_results, name='date_results'),
    url(r'^seasons/$', game_views.season_index, name='season_index'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(url(r'^debug/', include(debug_toolbar.urls)))
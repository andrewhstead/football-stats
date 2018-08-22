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
from games import views as games_views
from home import views as home_views
from django.views.static import serve
from .settings import MEDIA_ROOT

urlpatterns = [
    url(r'^$', home_views.home_page, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    url(r'^tables/', games_views.league_tables, name='league_tables'),
    url(r'^table/(?P<country>.*)/(?P<competition>.*)/(?P<season>.*)/$', games_views.competition_table, name='competition_table'),
    url(r'^results/$', games_views.latest_results, name='latest_results'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(url(r'^debug/', include(debug_toolbar.urls)))
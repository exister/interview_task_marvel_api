# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url


urlpatterns_auth = patterns('mr_api.api.auth',
    url('^auth/login/$', 'login_api_view', name='auth-login'),
    url('^auth/logout/$', 'logout_api_view', name='auth-logout'),
)

urlpatterns_comics = patterns('mr_api.api.comics',
    url('^m/comics/$', 'comics_list_api_view', name='m-comics'),
    url('^m/comics/(?P<id>\d+)/related/$', 'related_comics_list_api_view', name='m-related-comics'),
)

urlpatterns_characters = patterns('mr_api.api.characters',
    url('^m/characters/(?P<id>\d+)/events/$', 'character_events_list_api_view', name='m-character-events'),
)


urlpatterns = patterns('',)
urlpatterns += urlpatterns_auth
urlpatterns += urlpatterns_comics
urlpatterns += urlpatterns_characters

# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url


urlpatterns_auth = patterns('mr_api.api.auth',
    url('^auth/login/$', 'login_api_view', name='auth-login'),
    url('^auth/logout/$', 'logout_api_view', name='auth-logout'),
)


urlpatterns = patterns('',)
urlpatterns += urlpatterns_auth

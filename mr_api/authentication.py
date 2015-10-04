# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import jwt

from django.conf import settings
from django.utils.translation import ugettext as _
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header

from .models import AuthToken


class TokenAuthentication(BaseAuthentication):
    """
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """

    model = AuthToken

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'token':
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(auth[1])

    def authenticate_credentials(self, key):
        try:
            data = jwt.decode(key, settings.SECRET_KEY)
        except Exception as e:  # TODO log
            raise exceptions.AuthenticationFailed('Invalid token')

        try:
            token = self.model.objects.select_related('user')\
                .filter(user__is_active=True, user_id=data['user_id'])\
                .get(token=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token'))

        return token.user, token

    def authenticate_header(self, request):
        return 'Token'

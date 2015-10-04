import random
import datetime
import jwt
from django.conf import settings
from django.db import models


class AuthToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='auth_token')
    token = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_token()
        return super(AuthToken, self).save(*args, **kwargs)

    def generate_token(self):
        return jwt.encode({
            'user_id': self.user_id,
            'rnd': random.random(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }, settings.SECRET_KEY)

    def __unicode__(self):
        return self.token

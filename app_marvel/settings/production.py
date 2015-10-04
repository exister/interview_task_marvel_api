from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/data/db.sqlite3',
    }
}

MEDIA_ROOT = '/data/upload/'
STATIC_ROOT = '/data/static/'

ALLOWED_HOSTS = [
    '*',
]
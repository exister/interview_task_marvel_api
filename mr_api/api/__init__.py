from django.conf import settings
from marvel.marvel import Marvel


marvel_api = Marvel(settings.MARVEL_PUBLIC_KEY, settings.MARVEL_PRIVATE_KEY)

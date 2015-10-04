from django.conf import settings
from marvel.marvel import Marvel
from rest_framework_extensions.key_constructor import bits
from rest_framework_extensions.key_constructor.constructors import DefaultKeyConstructor

marvel_api = Marvel(settings.MARVEL_PUBLIC_KEY, settings.MARVEL_PRIVATE_KEY)


class CacheKeyConstructor(DefaultKeyConstructor):
    all_query_params = bits.QueryParamsKeyBit()

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from marvel.marvel import Marvel
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .mixins import Paginatable


m = Marvel(settings.MARVEL_PUBLIC_KEY, settings.MARVEL_PRIVATE_KEY)


class ComicsListAPIView(Paginatable, ListAPIView):
    limit = 10

    def list(self, request, *args, **kwargs):
        try:
            comics = m.get_comics(
                titleStartsWith=request.GET.get('title'),
                limit=self.limit,
                offset=(lambda x: max(int(x) * self.limit if x and x.isdigit() else 0, 0))(request.GET.get('page'))
            )
        except Exception as e:
            return Response({'error': e.message}, status=500)

        if comics.code != 200:
            return Response({'error': comics.status}, status=comics.code)

        return Response(comics.dict.get('data', {}))

comics_list_api_view = ComicsListAPIView.as_view()

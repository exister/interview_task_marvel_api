# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from urlparse import urlparse
from django.conf import settings
from marvel.marvel import Marvel
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .mixins import Paginatable


m = Marvel(settings.MARVEL_PUBLIC_KEY, settings.MARVEL_PRIVATE_KEY)


class ListView(Paginatable, ListAPIView):
    limit = 10

    def get_page_filters(self, request):
        return {
            'limit': self.limit,
            'offset': (lambda x: max(int(x) * self.limit if x and x.isdigit() else 0, 0))(request.GET.get('page'))
        }

    def load_list(self, filters):
        try:
            comics = m.get_comics(**filters)
        except Exception as e:
            return Response({'error': e.message}, status=500)

        if comics.code != 200:
            return Response({'error': comics.status}, status=comics.code)

        return Response(comics.dict.get('data', {}))


class ComicsListAPIView(ListView):

    def list(self, request, *args, **kwargs):
        filters = self.get_page_filters(request)
        if request.GET.get('title'):
            filters['titleStartsWith'] = request.GET.get('title')

        return self.load_list(filters)

comics_list_api_view = ComicsListAPIView.as_view()


class RelatedComicsListAPIView(ListView):
    def get_comic(self, comic_id):
        comic = None

        if comic_id:
            try:
                comic = m.get_comic(comic_id)
            except Exception as e:  # TODO log
                pass
            else:
                if comic.code != 200:
                    comic = None

        return comic

    def list(self, request, *args, **kwargs):
        comic = self.get_comic(kwargs.get('id'))

        if not comic:
            return Response({'error': 'Not found'}, status=404)

        def build_ids_list(items):
            def extract_id(item):
                if item.get('role') == 'writer':
                    url = item.get('resourceURI')
                    if url:
                        u = urlparse(url)
                        return u.path.split('/')[-1]

                return None

            return ','.join(filter(lambda x: x and x.isdigit(), map(extract_id, items)))

        filters = self.get_page_filters(request)
        related_filters = {
            'creators': build_ids_list(comic.data.result.creators.dict['items']),
            'characters': build_ids_list(comic.data.result.characters.dict['items']),
            'series': build_ids_list([comic.data.result.series])
        }
        for f, v in related_filters.items():
            if v:
                filters[f] = v

        return self.load_list(filters)

related_comics_list_api_view = RelatedComicsListAPIView.as_view()

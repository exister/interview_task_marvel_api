# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from urlparse import urlparse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_extensions.cache.decorators import cache_response
from .mixins import Paginatable
from . import marvel_api, CacheKeyConstructor


class ListView(Paginatable, APIView):
    def load_list(self, filters):
        try:
            comics = marvel_api.get_comics(**filters)
        except Exception as e:
            return Response({'error': e.message}, status=500)

        if comics.code != 200:
            return Response({'error': comics.status}, status=comics.code)

        return Response(comics.dict.get('data', {}))


class ComicsListAPIView(ListView):
    @cache_response(key_func=CacheKeyConstructor())
    def get(self, request, *args, **kwargs):
        """
        Comics list resource.
        ---
        type:
          count:
            type: integer
          total:
            type: integer
          limit:
            type: integer
          offset:
            type: integer
          results:
            type: array

        parameters:
            - name: title
              description: Case-sensitive title
              required: false
              type: string
              paramType: query
            - name: page
              description: Page number
              required: false
              type: integer
              paramType: query
        """

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
                comic = marvel_api.get_comic(comic_id)
            except Exception as e:  # TODO log
                pass
            else:
                if comic.code != 200:
                    comic = None

        return comic

    @cache_response(key_func=CacheKeyConstructor())
    def get(self, request, *args, **kwargs):
        """
        ---
        parameters:
            - name: page
              description: Page number
              required: false
              type: integer
              paramType: query
        """
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

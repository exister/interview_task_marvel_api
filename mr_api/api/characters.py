# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from marvel.character import Character
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .mixins import Paginatable
from . import marvel_api


class ListView(Paginatable, ListAPIView):
    def load_list(self, char_id, filters):
        if not char_id:
            return Response({'error': 'No character id'}, status=400)

        character = Character(marvel_api, {'id': char_id})

        try:
            r = character.get_events(**filters)
        except Exception as e:
            return Response({'error': e.message}, status=500)

        if r.code != 200:
            return Response({'error': r.status}, status=r.code)

        return Response(r.dict.get('data', {}))


class CharacterEventsListAPIView(ListView):

    def list(self, request, *args, **kwargs):
        filters = self.get_page_filters(request)
        return self.load_list(kwargs.get('id'), filters)

character_events_list_api_view = CharacterEventsListAPIView.as_view()

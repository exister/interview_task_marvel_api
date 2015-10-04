# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class Paginatable(object):
    limit = 10

    def get_page_filters(self, request):
        return {
            'limit': self.limit,
            'offset': (lambda x: max(int(x) * self.limit if x and x.isdigit() else 0, 0))(request.GET.get('page'))
        }

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
from boogie.rest import rest_api
from rest_framework.response import Response

from .filters import *

class CandidatesConfig(AppConfig):
    name = 'ej_candidates'
    verbose_name = _('Candidates')
    api = None

    def ready(self):
        from . import api
        from ej_candidates.models.candidate import Candidate
        # overwrite boogie viewset, and use besouro implementation.
        # This is necessary to filter candidates for unlogged users.
        def list(self, request):
            rest_api_v1 = rest_api.get_api_info('v1')
            serializer = rest_api_v1.serializer_class(Candidate)
            try:
                limit = int(request.GET.get("limit"))
            except:
                limit = 10
            querySet = Candidate.objects.all()
            filters = get_filters(request.GET)
            if (valid_filters(filters)):
                result = filter_candidates(querySet, filters)
                if (result):
                    querySet = result.order_by("-id")[:limit]
                    return Response(serializer(querySet, many=True,
                                            context={'request': request}).data)
                else:
                    return Response([])
            else:
                # order_by('?') randomize the querySet result.
                # This is not the best aproach, but
                # 9000 candidates are few data to retrieve.
                querySet = querySet.order_by('?')[:limit]
                return Response(serializer(querySet, many=True, 
                                           context={'request': request}).data)
        self.api = api
        rest_api_v1 = rest_api.get_api_info('v1')
        candidate_view_set = rest_api_v1.viewset_class(Candidate)
        candidate_view_set.list = list


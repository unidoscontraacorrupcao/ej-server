from boogie.router import Router
from .filters import *
from django.http import Http404, JsonResponse
from rest_framework import status
import json
from .models.candidate import Candidate

app_name = 'ej_candidates'
urlpatterns = Router()

@urlpatterns.route('total-filtered-candidates')
def total_filtered_candidates(request):
	querySet = Candidate.objects.all()
	filters = get_filters(request.GET)
	if (valid_filters(filters)):
		try:
			total = filter_candidates(querySet, filters).count()
			return JsonResponse({'total': total}, status=status.HTTP_200_OK)
		except:
			return JsonResponse({'total': 0}, status=status.HTTP_200_OK)
	else:
		total = Candidate.objects.all().count()
		return JsonResponse({'total': total}, status=status.HTTP_200_OK)
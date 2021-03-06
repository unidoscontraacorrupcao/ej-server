from boogie.rest import rest_api
from django.http import JsonResponse
import json

from .models.candidate import Candidate
from .models.selected_candidates import SelectedCandidate
from .models.pressed_candidates import PressedCandidate
from .models.favorite_candidates import FavoriteCandidate
from .filters import *

@rest_api.action('ej_users.User')
def candidates(request, user):
    limit = get_query_limit(request)
    querySet = Candidate.objects.exclude(favoritecandidate__user_id=user.id)
    filters = get_filters(request.GET)
    if (valid_filters(filters)):
        result = filter_candidates(querySet, filters);
        if (result):
            return result.order_by('?')[:limit]
        else:
            return []
    else:
        # order_by('?') randomize the querySet result.
        # This is not the best aproach, but
        # 9000 candidates are few data to retrieve.
        return querySet.order_by('?')[:limit]

@rest_api.action('ej_users.User')
def selected_candidates(request, user):
    limit = get_query_limit(request)
    querySet = Candidate.objects.filter(selectedcandidate__user_id=user.id)\
        .exclude(favoritecandidate__user_id=user.id)
    filters = get_filters(request.GET)
    if (valid_filters(filters)):
        result = filter_candidates(querySet, filters);
        if (result):
            return result.order_by("-id")[:limit]
        else:
            return []
    else:
        return querySet.order_by("-id")[:limit]

@rest_api.action('ej_users.User')
def total_selected_candidates(request, user):
    querySet = Candidate.objects.filter(selectedcandidate__user_id=user.id).count()
    return {'total': querySet}

@rest_api.action('ej_users.User')
def total_favorite_candidates(request, user):
    querySet = Candidate.objects.filter(favoritecandidate__user_id=user.id).count()
    return {'total': querySet}

@rest_api.action('ej_users.User')
def favorite_candidates(request, user):
    limit = get_query_limit(request)
    querySet = Candidate.objects.filter(favoritecandidate__user_id=user.id)
    filters = get_filters(request.GET)
    if (valid_filters(filters)):
        result = filter_candidates(querySet, filters);
        if (result):
            return result.order_by('?')[:limit]
        else:
            return []
    else:
        # order_by('?') randomize the querySet result.
        # This is not the best aproach, but
        # 9000 candidates are few data to retrieve.
        return querySet.order_by('?')[:limit]
@rest_api.action('ej_users.User', methods=['post'])
def unselect_candidate(request, user):
    candidate = json.loads(request.body.decode("utf8"))["candidate"]
    SelectedCandidate.objects.get(candidate=candidate, user=user).delete()

@rest_api.action('ej_users.User', methods=['post'])
def unfavorite_candidate(request, user):
    candidate = json.loads(request.body.decode("utf8"))["candidate"]
    FavoriteCandidate.objects.get(candidate=candidate, user=user).delete()

@rest_api.action('ej_candidates.Candidate', methods=['get'])
def status(request, candidate):
    status = ''
    user = request.GET.get('user')
    try:
        SelectedCandidate.objects.get(user_id=user, candidate_id=candidate)
        status = 'selected'
    except Exception as e:
        try:
            PressedCandidate.objects.get(user_id=user, candidate_id=candidate)
            status = 'pressed'
        except Exception as e:
            status = 'unselected'

    return {'status': status}

@rest_api.action('ej_candidates.Candidate', methods=['get'])
def metrics(request, candidate):
    selected_count = SelectedCandidate.objects.filter(candidate_id=candidate).count()
    pressed_count = PressedCandidate.objects.filter(candidate_id=candidate).count()
    favorite_count = FavoriteCandidate.objects.filter(candidate_id=candidate).count()
    return {'selected_count': selected_count, 'pressed_count': pressed_count, 'fav_count': favorite_count}

@rest_api.action('ej_users.User', methods=['get'])
def total_filtered_candidates(request, user):
	querySet = Candidate.objects.exclude(favoritecandidate__user_id=user.id)
	filters = get_filters(request.GET)
	if(valid_filters(filters)):
		try:
			total = filter_candidates(querySet, filters).count()
			return {'total': total}
		except:
			return {'total': 0}
	else:
		total = Candidate.objects.all().count()
		return {'total': total}

@rest_api.action('ej_users.User', methods=['get'])
def is_favorite(request, user):
    candidate = request.query_params["candidate"]
    try:
        querySet = FavoriteCandidate.objects.get(candidate_id=candidate, user=user)
        return {'is_favorite': True}
    except:
        return {'is_favorite': False}
        

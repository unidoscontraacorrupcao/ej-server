from boogie.rest import rest_api
import json

from .models.candidate import Candidate
from .models.selected_candidates import SelectedCandidate
#
# User extra actions and attributes
#

@rest_api.action('ej_users.User')
def candidates(request, user):
    querySet = Candidate.objects.exclude(selectedcandidate__user_id=user.id)\
        .exclude(pressedcandidate__user_id=user.id)
    return querySet.exclude(ignoredcandidate__user_id=user.id)

@rest_api.action('ej_users.User')
def selected_candidates(request, user):
    return Candidate.objects.filter(selectedcandidate__user_id=user.id)

@rest_api.action('ej_users.User', methods=['post'])
def unselect_candidate(request, user):
    candidate = json.loads(request.body.decode("utf8"))["candidate"]
    SelectedCandidate.objects.get(candidate=candidate, user=user).delete()

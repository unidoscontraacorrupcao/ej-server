from django.db import models
from ej_users.models import User
from .candidate import Candidate

from boogie import rules
from boogie.rest import rest_api

@rest_api()
class FavoriteCandidate(models.Model):

    """Favorite candidates by a user"""
    def __str__(self):
        return "%s - %s" % (self.candidate.name, self.candidate.party)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=True)
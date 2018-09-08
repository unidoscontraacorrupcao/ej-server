from django.db import models
from ej_users.models import User
from .candidate import Candidate
from django.db.models.signals import pre_save
from django.dispatch import receiver

from boogie import rules
from boogie.rest import rest_api

@rest_api()
class FavoriteCandidate(models.Model):

    """Favorite candidates by a user"""
    def __str__(self):
        return "%s - %s" % (self.candidate.name, self.candidate.party)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=True)

@receiver(pre_save, sender=FavoriteCandidate)
def validate_unique_together(sender, instance, **kwargs):
        candidates = FavoriteCandidate.objects.filter(candidate_id=instance.candidate.id,
                                      user_id=instance.user.id)
        if (len(candidates) > 0):
            raise Exception('Candidato já favoritado')
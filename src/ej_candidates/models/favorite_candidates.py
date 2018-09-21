from django.db import models
from ej_users.models import User
from .candidate import Candidate
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from ej_messages.models import Message
from ej_channels.models import Channel

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

@receiver(post_save, sender=FavoriteCandidate)
def send_message(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        body = instance.candidate.name
        target = instance.candidate.id
        try:
            channel = Channel.objects.filter(owner=user, sort="favorite")[0]
        except IndexError:
            channel = Channel.objects.create(name="favorite channel", sort="favorite", owner=user)
            channel.users.add(user)
            channel.save()
        Message.objects.create(channel=channel, title="", body=body, link="", target=target)
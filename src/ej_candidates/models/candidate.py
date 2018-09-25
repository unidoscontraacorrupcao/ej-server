from django.db import models
from model_utils import Choices
from model_utils.fields import StatusField
from django.db.models.signals import pre_save
from django.dispatch import receiver
from ej_messages.models import Message
from ej_channels.models import Channel
from ej_profiles.models import Setting
from push_notifications.models import GCMDevice


from boogie import rules
from boogie.rest import rest_api

@rest_api(
    ['id', 'name', 'candidacy', 'urn', 'party', 'image',
     'has_clean_pass', 'committed_to_democracy', 'uf',
     'full_name', 'occupation', 'justify_adhered_to_the_measures', 'lawsuits',
     'riches', 'adhered_to_the_measures', 'site_url', 'youtube_url', 'facebook_url',
     'crowdfunding_url', 'twitter_url', 'instagram_url']
)
class Candidate(models.Model):

    """A political candidate. """

    def __str__(self):
        return "%s - %s" % (self.name, self.party)

    CANDIDACY_OPTIONS = Choices('SENADOR(A)', 'DEPUTADO(A)')
    PARTY_OPTIONS = Choices('PT', 'PSDB')
    POLITICAL_OPTIONS = Choices('SIM', 'NÃO', 'SEM RESPOSTA')

    name = models.CharField(max_length=200,
                            help_text="The urn name of the candidate")
    full_name = models.CharField(max_length=200,
                            help_text="The full name of the candidate",
                            default="")
    occupation  = models.CharField(max_length=200,
                                   help_text="The occupation of the candidate",
                                   default="")

    candidacy = StatusField(choices_name='CANDIDACY_OPTIONS',
                            help_text="the candadite candidacy")
    urn = models.IntegerField(help_text="The candidate urn number")
    party = StatusField(choices_name='PARTY_OPTIONS',
                        help_text="The candidate party initials")
    image = models.FileField(upload_to="candidates", default="card_avatar-default.png")
    has_clean_pass = StatusField(choices_name='POLITICAL_OPTIONS')
    committed_to_democracy = StatusField(choices_name='POLITICAL_OPTIONS')
    adhered_to_the_measures = StatusField(choices_name='POLITICAL_OPTIONS')
    justify_adhered_to_the_measures = models.CharField(max_length=500,
                                                       help_text="Justification from the candidate",
                                                       default="")
    riches = models.CharField(max_length=500,
                              help_text="Candidate riches",
                              default="")
    lawsuits = models.CharField(max_length=500,
                                help_text="Candidate lawsuits",
                                default="")
    site_url = models.CharField(max_length=100,
                                help_text="The site of the candidate",
                                default="")
    uf = models.CharField(max_length=2,
                          help_text="The candidate uf",
                          default="")
    crowdfunding_url = models.CharField(max_length=200,
                                        help_text="The candidate crowdfunding",
                                        default="")
    facebook_url = models.CharField(max_length=200,
                                    help_text="The candidate facebook page",
                                    default="")
    twitter_url = models.CharField(max_length=200,
                                   help_text="The candidate facebook page",
                                   default="")
    instagram_url = models.CharField(max_length=200,
                                     help_text="The candidate instagram page",
                                     default="")
    youtube_url = models.CharField(max_length=200,
                                   help_text="The candidate instagram page",
                                   default="")
    public_email = models.CharField(max_length=200,
                                   help_text="The candidate public email",
                                   default="ricardo@cidadedemocratica.org.br")
    cpf = models.CharField(max_length=11,
                          help_text="The candidate cpf",
                          default='00000000000')

# boogie decorator to add a property on model serializer
@rest_api.property(Candidate)
def score(object):
    has_clean_pass_options = ["NÂO", "CONDENADO", "RÉ", "RÉU"]
    if (object.has_clean_pass == "SIM" \
            and object.committed_to_democracy == "SIM" \
            and object.adhered_to_the_measures == "SIM"):
        return 'good'
    if (object.has_clean_pass in has_clean_pass_options \
            or object.committed_to_democracy == "NÃO" \
            or object.adhered_to_the_measures == "NÃO"):
        return 'bad'
    return 'partial'

@receiver(pre_save, sender=Candidate)
def check_candidate_status_changed(sender, instance, **kwargs):
    try:
        old_candidate = Candidate.objects.filter(uf=instance.uf, urn=instance.urn)[0]
        if((old_candidate.committed_to_democracy == "SEM RESPOSTA" \
                and instance.committed_to_democracy == "SIM") \
                or (old_candidate.adhered_to_the_measures == "SEM RESPOSTA" \
                and instance.adhered_to_the_measures == "SIM")):
            send_message_to_users(old_candidate)
    except:
        pass

def send_message_to_users(candidate):
    #avoid circular import
    from .pressed_candidates import PressedCandidate
    sort = "candidate-pressed-" + str(candidate.urn) + "-" + candidate.uf
    try:
        channel = Channel.objects.get(sort=sort)
        send_fcm_message(channel, candidate)
        if(channel.users):
            Message.objects.create(channel=channel, title="", body=candidate.name, target=candidate.id)
            pressed = PressedCandidate.objects.filter(candidate=candidate)
            channel.users.clear()
            channel.save()
            pressed.delete()
    except:
        pass

def send_fcm_message(channel, candidate):
    users_to_send = []
    if(channel.users):
        for user in channel.users.all():
            setting = Setting.objects.get(owner_id=user.id)
            if (setting.disapproved_notifications == True):
                users_to_send.append(user)
        url = "https://app.unidoscontraacorrupcao.org.br/candidate/" + str(candidate.id)
        title = candidate.name + " se comprometeu"
        body = "Gostaria de reavaliar como candidato?"
        fcm_devices = GCMDevice.objects.filter(cloud_message_type="FCM", user__in=users_to_send)
        fcm_devices.send_message("", extra={"title": title, "body": body,
				"icon":"https://i.imgur.com/D1wzP69.png", "click_action": url})

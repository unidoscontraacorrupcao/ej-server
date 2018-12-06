import logging
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from ej_users.models import User
from ej_conversations.models.conversation import Conversation
from ej_messages.models import Message
from ej_channels.models import Channel
from ej_trophies.models.trophy import Trophy
from ej_trophies.models.user_trophy import UserTrophy
from ckeditor.fields import RichTextField
from .mixins import MissionMixin
from push_notifications.models import APNSDevice, GCMDevice
from ej_profiles.models import Setting

def mission_directory_path(instance, filename):
    return 'uploads/mission_{0}/{1}'.format(instance.mission.id, filename)

class Mission(MissionMixin, models.Model):

    title = models.CharField(max_length=100)
    description = RichTextField(max_length=1000)
    reward = RichTextField(max_length=1000, null=True)
    #who is doing the mission
    users = models.ManyToManyField(User, blank=True)
    youtubeVideo = models.CharField(max_length=60, blank=True, null=True)
    image = models.FileField(upload_to="missions",
                                  default="default.jpg")
    audio = models.FileField(upload_to="missions",
                                  default="default.jpg")
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="owner", null=True)
    trophy = models.ForeignKey(Trophy, on_delete=models.CASCADE, null=True)
    deadline = models.DateField(null=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    conversations = models.ManyToManyField(Conversation, blank=True)

    class Meta:
        ordering = ['title']

class Receipt(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    userName = models.CharField(max_length=30)
    userEmail = models.CharField(max_length=60)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=60)
    description = models.CharField(max_length=60)
    receiptFile  = models.FileField(upload_to="media/missions",
                                    default="media/default.jpg")

class Comment(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=280)

def update_automatic_trophies(user):
    def filter_trophies(user_trophy):
        return (user_trophy.trophy.key == req.key)
    automatic_trophies = Trophy.objects.filter(complete_on_required_satisfied=True)
    user_trophies = UserTrophy.objects.filter(percentage=100, user=user).all()
    for trophy in automatic_trophies:
        filtered_trophies = []
        required_trophies = trophy.required_trophies.all()
        for req in required_trophies:
            filtered = list(filter(filter_trophies, list(user_trophies)))
            if len(filtered) > 0:
                filtered_trophies.append(filtered)
        if (len(filtered_trophies) == len(required_trophies)):
            existent_user_trophy = UserTrophy.objects.filter(user=user,
                                                             trophy=trophy,
                                                             percentage=100)
            if (len(existent_user_trophy) == 0):
                user_trophy = UserTrophy(user=user,
                                        trophy=trophy,
                                        percentage=100,
                                        notified=True)
                user_trophy.save()
                send_trophy_message(user, user_trophy)

def send_trophy_message(user, user_trophy):
    try:
        channel = Channel.objects.filter(owner=user, sort="trophy")[0]
    except IndexError:
        channel = Channel.objects.create(name="trophy channel", sort="trophy", owner=user)
        channel.users.add(user)
        channel.save()
    trophy_name = user_trophy.trophy.name
    trophy_id = user_trophy.trophy.id
    Message.objects.create(channel=channel, title="", body=trophy_name, target=trophy_id)

@receiver(post_save, sender=Receipt)
def update_trophy(sender, **kwargs):
    instance = kwargs.get('instance')
    if (instance.status == "realized"):
        mission_trophy = instance.mission.trophy
        user = instance.user
        user_trophy = UserTrophy.objects.get(trophy=mission_trophy,
                                             user=user)
        user_trophy.percentage = 100
        user_trophy.save()
        update_automatic_trophies(user)
        send_trophy_message(user, user_trophy)

@receiver(post_save, sender=Mission)
def create_conversation_channel(sender, instance, created, **kwargs):
    sort = "conversation-" + str(instance.id)
    try:
        Channel.objects.filter(name="converstion channel", sort=sort)[0]
    except IndexError:
        Channel.objects.create(name="converstion channel", sort=sort)

@receiver(post_save, sender=Mission)
def send_message(sender, instance, created, **kwargs):
    if created:
        channel = Channel.objects.get(sort="mission")
        mission_title = instance.title
        mission_id = instance.id
        Message.objects.create(channel=channel, title="", body=mission_title, target=mission_id)

@receiver(post_save, sender=Mission)
def send_mission_fcm_message(sender, instance, created, **kwargs):
    if created:
        channel = Channel.objects.get(sort="mission")
        users_to_send = []
        for user in channel.users.all():
            try:
                setting = Setting.objects.get(owner_id=user.id)
                if (setting.mission_notifications == True):
                    users_to_send.append(user)
            except:
                pass
        url = "https://app.unidoscontraacorrupcao.org.br/show-mission/" + str(instance.id)
        try:
            fcm_devices = GCMDevice.objects.filter(cloud_message_type="FCM", user__in=users_to_send)
            fcm_devices.send_message("", extra={"title":"Nova missão", "body": "Nova missão no ar! Vem conferir",
                "icon":"https://i.imgur.com/D1wzP69.png", "click_action": url})
        except:
            pass

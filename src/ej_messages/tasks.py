from django_q.tasks import schedule
from push_notifications.models import APNSDevice, GCMDevice
import time

from ej_users.models import User
from ej_channels.models import Channel
from ej_profiles.models import Setting

def notification_task(channel_id, instance_id, created):
  if created:
    from ej_notifications.models import Notification
    from ej_messages.models import Message
    channel = Channel.objects.get(id=channel_id)
    instance = Message.objects.get(pk=instance_id)
    for user in channel.users.all():
      Notification.objects.create(receiver=user,
                                  channel=channel, message=instance)

def fcm_notification_task(channel_id, instance_id, created):
  if created:
    from ej_messages.models import Message
    channel = Channel.objects.get(id=channel_id)
    if channel.sort == 'admin':
      users_to_send = []
      for user in channel.users.all():
        try:
          setting = Setting.objects.get(owner_id=user.id)
          if (setting.admin_notifications == True):
            users_to_send.append(user)
        except:
          pass
      instance = Message.objects.get(pk=instance_id)
      fcm_devices = GCMDevice.objects.filter(cloud_message_type="FCM", user__in=users_to_send)
      send_notifications_in_batches(users_to_send, instance)

def send_notifications_in_batches(users, instance):
  limit_of_devices = 1000
  for user in range(len(users)):
    if len(users) < limit_of_devices:
      fcm_devices = GCMDevice.objects.filter(cloud_message_type="FCM", user__in=users)
      fcm_devices.send_message("", extra={"title": instance.title, "body": instance.body,
                                        "icon":"https://i.imgur.com/D1wzP69.png", "click_action": instance.link})
      break
    else:
      users_to_notify = []
      for batch_device in range(limit_of_devices):
        devices_to_notify << users.pop()
      fcm_devices = GCMDevice.objects.filter(cloud_message_type="FCM", user__in=users_to_notify)
      fcm_devices.send_message("", extra={"title": instance.title, "body": instance.body,
                                        "icon":"https://i.imgur.com/D1wzP69.png", "click_action": instance.link})
      time.sleep(60)

def create_notifications_task(message, created):
  schedule('ej_messages.models.notification_task',
           message.channel.id, message.id, True,
           schedule_type='M', minutes=1, repeats=-1)

def create_fcm_notifications_task(message, created):
  schedule('ej_messages.models.fcm_notification_task',
           message.channel.id, message.id, created,
           schedule_type='M', minutes=1, repeats=-1)

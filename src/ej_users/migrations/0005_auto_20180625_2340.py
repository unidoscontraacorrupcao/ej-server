# Generated by Django 2.0.6 on 2018-06-25 23:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ej_users', '0004_auto_20180621_0221'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermission',
            name='mission',
        ),
        migrations.RemoveField(
            model_name='usermission',
            name='user',
        ),
        migrations.RemoveField(
            model_name='user',
            name='missions',
        ),
        migrations.DeleteModel(
            name='UserMission',
        ),
    ]

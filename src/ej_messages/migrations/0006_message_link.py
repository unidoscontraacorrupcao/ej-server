# Generated by Django 2.0.6 on 2018-08-28 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ej_messages', '0005_message_target'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='link',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]

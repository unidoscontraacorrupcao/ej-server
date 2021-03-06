# Generated by Django 2.0.7 on 2018-08-03 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ej_users', '0008_userconversations_last_viewed_conversation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='display_name',
            field=models.CharField(help_text='A randomly generated name used to identify each user.', max_length=140, verbose_name='Display name'),
        ),
    ]

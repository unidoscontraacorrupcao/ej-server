# Generated by Django 2.0.6 on 2018-07-09 17:15

import django.core.validators
from django.db import migrations, models
import ej_conversations.validators


class Migration(migrations.Migration):

    dependencies = [
        ('ej_conversations', '0006_auto_20180611_0226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(help_text='Body of text for the comment', max_length=210, validators=[django.core.validators.MinLengthValidator(2), ej_conversations.validators.is_not_empty], verbose_name='Content'),
        ),
    ]

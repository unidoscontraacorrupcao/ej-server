# Generated by Django 2.0.7 on 2018-07-30 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ej_users', '0007_auto_20180730_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='userconversations',
            name='last_viewed_conversation',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]

# Generated by Django 2.0.6 on 2018-06-20 03:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ej_missions', '0002_auto_20180620_0326'),
        ('ej_users', '0002_auto_20180529_0043'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ej_missions.Mission')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='missions',
            field=models.ManyToManyField(through='ej_users.UserMissions', to='ej_missions.Mission'),
        ),
    ]

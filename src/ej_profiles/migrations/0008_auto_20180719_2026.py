# Generated by Django 2.0.6 on 2018-07-19 20:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ej_profiles', '0007_setting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ej_profiles.Profile'),
        ),
    ]
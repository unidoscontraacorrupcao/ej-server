# Generated by Django 2.0.5 on 2018-05-27 21:50

import boogie.fields.enum_field
from django.db import migrations, models
import ej_profiles.choices


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('race', boogie.fields.enum_field.EnumField(ej_profiles.choices.Race, default=ej_profiles.choices.Race(0), verbose_name='Race')),
                ('gender', boogie.fields.enum_field.EnumField(ej_profiles.choices.Gender, default=ej_profiles.choices.Gender(0), verbose_name='Gender identity')),
                ('gender_other', models.CharField(blank=True, max_length=50, verbose_name='User provided gender')),
                ('age', models.IntegerField(blank=True, null=True, verbose_name='Age')),
                ('country', models.CharField(blank=True, max_length=50, verbose_name='Country')),
                ('state', models.CharField(blank=True, max_length=140, verbose_name='State')),
                ('city', models.CharField(blank=True, max_length=140, verbose_name='City')),
                ('biography', models.TextField(blank=True, verbose_name='Biography')),
                ('occupation', models.CharField(blank=True, max_length=50, verbose_name='Occupation')),
                ('political_activity', models.TextField(blank=True, verbose_name='Political activity')),
                ('image', models.ImageField(blank=True, null=True, upload_to='profile_images', verbose_name='Image')),
            ],
        ),
    ]

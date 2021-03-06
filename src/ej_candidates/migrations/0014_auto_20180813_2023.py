# Generated by Django 2.0.7 on 2018-08-13 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ej_candidates', '0013_auto_20180810_2212'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='crowdfunding_url',
            field=models.CharField(default='', help_text='The candidate crowdfunding', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='candidate',
            name='facebook_url',
            field=models.CharField(default='', help_text='The candidate facebook page', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='candidate',
            name='instagram_url',
            field=models.CharField(default='', help_text='The candidate instagram page', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='candidate',
            name='twitter_url',
            field=models.CharField(default='', help_text='The candidate facebook page', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='candidate',
            name='uf',
            field=models.CharField(default='', help_text='The candidate uf', max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='candidate',
            name='youtube_url',
            field=models.CharField(default='', help_text='The candidate instagram page', max_length=30),
            preserve_default=False,
        ),
    ]

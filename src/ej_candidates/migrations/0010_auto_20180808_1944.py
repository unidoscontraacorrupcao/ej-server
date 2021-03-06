# Generated by Django 2.0.7 on 2018-08-08 19:44

from django.db import migrations
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ej_candidates', '0009_auto_20180808_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='adhered_to_the_measures',
            field=model_utils.fields.StatusField(choices=[(0, 'dummy')], default='sim', max_length=100, no_check_for_status=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='committed_to_democracy',
            field=model_utils.fields.StatusField(choices=[(0, 'dummy')], default='sim', max_length=100, no_check_for_status=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='has_clean_pass',
            field=model_utils.fields.StatusField(choices=[(0, 'dummy')], default='sim', max_length=100, no_check_for_status=True),
        ),
    ]

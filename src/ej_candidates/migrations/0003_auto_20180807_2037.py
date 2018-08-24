# Generated by Django 2.0.7 on 2018-08-07 20:37

from django.db import migrations, models
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ej_candidates', '0002_auto_20180807_2023'),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The name of the candidate', max_length=100)),
                ('candidacy', model_utils.fields.StatusField(choices=[('senadora', 'senadora')], default='senadora', help_text='the candadite candidacy', max_length=100, no_check_for_status=True)),
                ('urn', models.IntegerField(help_text='The candidate urn number')),
                ('party', model_utils.fields.StatusField(choices=[('pt', 'pt'), ('psdb', 'psdb')], default='pt', help_text='The candidate party initials', max_length=100, no_check_for_status=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Candidates',
        ),
    ]
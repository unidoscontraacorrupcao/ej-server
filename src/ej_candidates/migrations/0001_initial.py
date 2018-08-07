# Generated by Django 2.0.7 on 2018-08-07 20:09

from django.db import migrations, models
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The name of the candidate', max_length=100)),
                ('candidacy', model_utils.fields.StatusField(choices=[('senadora', 'senadora')], default='senadora', max_length=100, no_check_for_status=True)),
                ('urn', models.IntegerField()),
                ('party', model_utils.fields.StatusField(choices=[('pt', 'pt'), ('psdb', 'psdb')], default='pt', max_length=100, no_check_for_status=True)),
            ],
        ),
    ]

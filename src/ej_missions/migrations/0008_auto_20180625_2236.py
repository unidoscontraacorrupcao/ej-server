# Generated by Django 2.0.6 on 2018-06-25 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ej_missions', '0007_auto_20180625_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mission',
            name='fileUpload',
            field=models.FileField(default='media/default.jpg', upload_to='media/missions'),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='receiptFile',
            field=models.FileField(default='media/default.jpg', upload_to='media/missions'),
        ),
    ]

# Generated by Django 2.0.6 on 2018-06-25 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ej_missions', '0006_auto_20180623_0156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mission',
            name='fileUpload',
            field=models.FileField(default='missions/default.jpg', upload_to='missions'),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='receiptFile',
            field=models.FileField(default='missions/default.jpg', upload_to='missions'),
        ),
    ]

# Generated by Django 3.2.12 on 2022-04-19 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wotwatcher', '0004_auto_20220227_1028'),
    ]

    operations = [
        migrations.AddField(
            model_name='tankratingsubscription',
            name='defPerGame',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='tankratingsubscription',
            name='spotPerGame',
            field=models.FloatField(default=0),
        ),
    ]
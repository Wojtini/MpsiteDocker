# Generated by Django 3.2.12 on 2022-02-27 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wotwatcher', '0003_tankratingsubscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='tankratingsubscription',
            name='dmgPerGame',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tankratingsubscription',
            name='fragPerGame',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='tankratingsubscription',
            name='lastUpdate',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='tankratingsubscription',
            name='winRate',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='tankratingsubscription',
            name='wn8',
            field=models.IntegerField(default=0),
        ),
    ]
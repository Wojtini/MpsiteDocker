# Generated by Django 3.2.12 on 2022-04-06 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_profile_profile_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='EnvironmentVariable',
            fields=[
                ('name', models.TextField(primary_key=True, serialize=False)),
                ('value', models.JSONField()),
            ],
        ),
    ]

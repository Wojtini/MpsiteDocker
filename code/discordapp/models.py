from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class Playlist(models.Model):
    name = models.TextField(primary_key=True)
    desc = models.TextField(null=True)
    active = models.TextField(default=True)

    def __str__(self):
        return self.name


class PlaylistOwnership(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.playlist} permissions for {self.user}"


class Song(models.Model):
    name = models.TextField(null=False)
    url = models.TextField(null=False)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


admin.site.register(Song)
admin.site.register(PlaylistOwnership)
admin.site.register(Playlist)

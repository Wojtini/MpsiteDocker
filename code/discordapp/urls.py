from django.urls import path

from . import views

app_name = "discordapp"
urlpatterns = [
    path('', views.index, name='index'),
    path('playlists', views.playlist_list, name='playlist_list'),
    path('play/<str:playlist_name>', views.play_playlist, name='play_playlist'),
]


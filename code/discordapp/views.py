from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import requests

from discordapp.forms import AddSongForm
from home.models import EnvironmentVariable
import os
from discordapp.models import Playlist, PlaylistOwnership
from django.contrib.auth.models import User
from discordapp.models import Song
import json
from discordapp.bot_connector import bot_play_playlist, bot_skip, bot_stop


@login_required
def index(request):
    try:
        var = EnvironmentVariable.objects.filter(name="discordWOTCronChannel")[0]
    except IndexError:
        var = EnvironmentVariable()
        var.name = "discordWOTCronChannel"
        var.value = {'gid': None, 'tcid': None}
        var.save()
        var = EnvironmentVariable.objects.filter(name="discordWOTCronChannel")[0]

    try:
        r = requests.get(f'{os.environ.get("DSC_API_URL")}discord/guilds')
    except requests.ConnectionError as ex:
        print(ex)
        return redirect('home:index')
    data = r.json()

    if var.value['gid'] and var.value['tcid']:
        for guild in data:
            if int(guild['gid']) == int(var.value['gid']):
                guild['active'] = True
            for text_channel in guild['text_channels']:
                if int(text_channel['tcid']) == int(var.value['tcid']):
                    text_channel['active'] = True

    return render(request, "discord_index.html",
                  context={
                      'perm': data,
                  })


@login_required
def playlist_list(request):

    form = AddSongForm(request.POST or None)
    if form.is_valid():
        cd = form.cleaned_data
        new_song = Song()
        new_song.name = cd.get('name')
        new_song.playlist = cd.get('playlist')
        new_song.url = cd.get('url')
        new_song.save()

    playlists = Playlist.objects.all().values()
    owned_playlists = Playlist.objects.filter(playlistownership__user=request.user).values()
    for playlist in playlists:
        playlist['can_manage'] = playlist in owned_playlists
        songs = Song.objects.filter(playlist=playlist['name']).values()
        playlist['songs'] = songs

    return render(request, "playlist_list.html",
                  context={
                      'playlists': playlists,
                      'form': form,
                  })


@login_required
def play_playlist_view(request, playlist_name):
    bot_play_playlist(playlist_name)
    return redirect('discordapp:playlist_list')


@login_required
def skip_music_view(request):
    bot_skip()
    return redirect('discordapp:playlist_list')


@login_required
def stop_playlist_view(request):
    bot_stop()
    return redirect('discordapp:playlist_list')


@login_required
def add_song(request):
    form = AddSongForm(request.POST or None)
    if form.is_valid():
        cd = form.cleaned_data
        new_song = Song()
        new_song.name = cd.get('name')
        new_song.playlist = cd.get('playlist')
        new_song.url = cd.get('url')
        new_song.save()

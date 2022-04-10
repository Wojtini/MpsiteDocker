import json
import os
import requests

from discordapp.models import Song


def bot_play_playlist(playlist_name):
    songs = Song.objects.filter(playlist=playlist_name)
    params = {'playlist_name': playlist_name, 'songs': []}
    for song in songs:
        params['songs'].append({"name": song.name, "url": song.url})
    params = json.dumps(params)
    requests.put(f'{os.environ.get("DSC_API_URL")}music/play_playlist', json=params)


def bot_stop():
    requests.patch(f'{os.environ.get("DSC_API_URL")}music/stop')


def bot_skip():
    requests.patch(f'{os.environ.get("DSC_API_URL")}music/skip')


def bot_add_priority():
    pass



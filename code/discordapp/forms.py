from django import forms
from discordapp.models import Playlist


class AddSongForm(forms.Form):
    data = Playlist.objects.all()
    name = forms.CharField(label='Song Title', max_length=100, required=True)
    url = forms.CharField(label='Youtube url', max_length=180, required=True)
    playlist = forms.ModelChoiceField(queryset=data, required=True)

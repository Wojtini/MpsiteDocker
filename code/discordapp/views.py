from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import requests
from home.models import EnvironmentVariable
import os


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

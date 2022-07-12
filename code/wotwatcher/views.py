from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import WN8Form
from .models import TankExpectations, TankRatingSubscription
from .views_helpers import add_user_tank_to_database, update_wn8, get_wn8_color


@login_required
def add_menu(request):
    result_msg = ""
    form = WN8Form(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        wot_username = data.get('nick')
        tank_name = data.get('tank')
        result_msg = add_user_tank_to_database(tank_name, wot_username, request.user)
    return render(request, "wot_addmenu.html",
                  context={
                      'return_msg': result_msg,
                      'form': form,
                  })


# @login_required
def list_menu(request):
    subs = TankRatingSubscription.objects.all()
    result = {}
    for sub in subs:
        result[sub.wot_username] = []
    for sub in subs:
        exp_tank = TankExpectations.objects.filter(tank_name=sub.tank)[0]
        dict = {
            "username": sub.wot_username,
            "tank": sub.tank.tank_name,
            "wn8": sub.wn8,
            "wn8color": get_wn8_color(sub.wn8),
            "avgDmg": sub.dmgPerGame,
            "avgFrag": sub.fragPerGame,
            "avgWinRate": sub.winRate,
            "avgSpot": sub.spotPerGame,
            "avgDef": sub.defPerGame,
            'dif_Dmg': round(sub.dmgPerGame - exp_tank.exp_Damage, 2),
            'dif_Frag': round(sub.fragPerGame - exp_tank.exp_Frag, 2),
            'dif_expWinRate': round(sub.winRate - exp_tank.exp_WinRate, 2),
            'dif_expDef': round(sub.defPerGame - exp_tank.exp_Def, 2),
            'dif_expSpot': round(sub.spotPerGame - exp_tank.exp_Spot, 2),
        }
        result[sub.wot_username].append(dict)
    return render(request, "wot_tanklist.html", context={
                    "subs": result,
                })


@login_required
def update_request(request):
    update_wn8()
    return redirect('wotapi:list')

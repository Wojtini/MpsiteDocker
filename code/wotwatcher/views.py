from django.contrib.auth.decorators import login_required
from django.db.models.functions import datetime
from django.shortcuts import render, redirect

from .forms import WN8Form
from .wotconnector.wotconnector import get_acc_id, get_vehicle_stats
from .models import TankExpectations, TankRatingSubscription


# Create your views here.


@login_required
def add_menu(request):
    form = WN8Form(request.POST or None)
    exp_tank = None
    wn8 = 0
    vehstats = None
    id = None
    if form.is_valid():
        cd = form.cleaned_data
        # print(cd.get('tank'))
        try:
            id = get_acc_id(cd.get('nick'))
            exp_tank = TankExpectations.objects.filter(tank_name=cd.get('tank'))[0]
            vehstats = get_vehicle_stats(user_id=id, tank_id=exp_tank.tank_id)
            wn8 = calculate_wn8(
                tankId=exp_tank.tank_id,
                avgDmg=vehstats['damage_per_game'],
                avgFrag=vehstats['frags_per_game'],
                avgSpot=vehstats['spotted_per_game'],
                avgDef=vehstats['def_per_game'],
                avgWinRate=vehstats['winrate'],
            )
        except KeyError and IndexError and TypeError as Ex:

            pass


    return render(request, "wot_addmenu.html",
                  context={
                      'form': form,
                      'exp_tank': exp_tank,
                      'real_tank': vehstats,
                      'player_id': id,
                      'wn8': wn8,
                  })

    # wn8 = calculate_wn8(65329, 2000, 1, 1, 1, 50)
    # return render(request, "wot_addmenu.html", context={'wn8': wn8})

# @login_required
def list_menu(request):
    subs = TankRatingSubscription.objects.all()
    result = {}
    for sub in subs:
        result[sub.wot_username] = []
    for sub in subs:
        try:
            exp_tank = TankExpectations.objects.filter(tank_name=sub.tank)[0]
            dict = {
                "username": sub.wot_username,
                "tank": sub.tank.tank_name,
                "wn8": sub.wn8,
                "wn8color": get_wn8_color(sub.wn8),
                "avgDmg": sub.dmgPerGame,
                "avgFrag": sub.fragPerGame,
                "avgWinRate": sub.winRate,
                'dif_Dmg': round(sub.dmgPerGame - exp_tank.exp_Damage, 2),
                'dif_Frag': round(sub.fragPerGame - exp_tank.exp_Frag, 2),
                'dif_expWinRate': round(sub.winRate - exp_tank.exp_WinRate, 2),
            }
            result[sub.wot_username].append(dict)
        except TypeError:
            pass
    return render(request, "wot_tanklist.html", context={
        "subs": result,
    })

@login_required
def update_request(request):
    update_wn8()
    return redirect('wotapi:list')


def update_wn8():
    subs = TankRatingSubscription.objects.all()
    for sub in subs:
        try:
            wn8, data = get_wn8(sub.wot_username, sub.tank)
            sub.wn8 = wn8
            sub.lastUpdate = datetime.datetime.now()
            sub.dmgPerGame = data['avgDmg']
            sub.fragPerGame = data['avgFrag']
            sub.winRate = data['avgWinRate']
            sub.save()
        except TypeError:
            pass


def get_wn8(player, tank):
    try:
        id = get_acc_id(player)

        model = TankExpectations.objects.filter(tank_name=tank)[0]
        vehstats = get_vehicle_stats(user_id=id, tank_id=model.tank_id)

        wn8 = calculate_wn8(
            tankId=model.tank_id,
            avgDmg=vehstats['damage_per_game'],
            avgFrag=vehstats['frags_per_game'],
            avgSpot=vehstats['spotted_per_game'],
            avgDef=vehstats['def_per_game'],
            avgWinRate=vehstats['winrate'],
        )

        data = {
            'avgDmg': vehstats['damage_per_game'],
            'avgFrag': vehstats['frags_per_game'],
            'avgWinRate': vehstats['winrate'],
            # 'expDmg': model.exp_Damage,
            # 'expFrag': model.exp_Damage,
            # 'expWinRate': model.exp_Damage,
            'dif_Dmg': round(vehstats['damage_per_game'] - model.exp_Damage, 2),
            'dif_Frag': round(vehstats['frags_per_game'] - model.exp_Frag, 2),
            'dif_expWinRate': round(vehstats['winrate'] - model.exp_WinRate, 2),
        }
        return wn8, data
    except Exception as e:
        print(e)
        return -1


def get_wn8_color(value):
    if value < 300:
        return '#000000'
    elif value < 600:
        return '#CF3230'
    elif value < 900:
        return '#DC7500'
    elif value < 1250:
        return '#D8B502'
    elif value < 1600:
        return '#6D9524'
    elif value < 1900:
        return '#4C762E'
    elif value < 2350:
        return '#4A92BA'
    elif value < 2900:
        return '#84579C'
    else:
        return '#83579C'


def calculate_wn8(tankId, avgDmg, avgSpot, avgFrag, avgDef, avgWinRate):
    model = TankExpectations.objects.filter(tank_id=tankId)[0]
    rDAMAGE = avgDmg / model.exp_Damage
    rSPOT = avgSpot / model.exp_Spot
    rFRAG = avgFrag / model.exp_Frag
    rDEF = avgDef / model.exp_Def
    rWIN = avgWinRate / model.exp_WinRate

    # step 2

    rWINc = max(0, (rWIN - 0.71) / (1 - 0.71))
    rDAMAGEc = max(0, (rDAMAGE - 0.22) / (1 - 0.22))
    rFRAGc = max(0, min(rDAMAGEc + 0.2, (rFRAG - 0.12) / (1 - 0.12)))
    rSPOTc = max(0, min(rDAMAGEc + 0.1, (rSPOT - 0.38) / (1 - 0.38)))
    rDEFc = max(0, min(rDAMAGEc + 0.1, (rDEF - 0.10) / (1 - 0.10)))

    WN8 = 980 * rDAMAGEc + 210 * rDAMAGEc * rFRAGc + 155 * rFRAGc * rSPOTc + 75 * rDEFc * rFRAGc + 145 * min(1.8,
                                                                                                             rWINc)

    return round(WN8)

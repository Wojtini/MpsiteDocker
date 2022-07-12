import datetime

from wot_api.wotconnector import get_acc_id_by_name, get_vehicle_stats, get_vehicles_stats
from wotwatcher.models import TankExpectations, TankRatingSubscription


def add_user_tank_to_database(tank_name: str, wot_username: str, site_username: str) -> str:
    exp_tank = get_tank_from_name(tank_name)

    if len(TankRatingSubscription.objects.filter(wot_username=wot_username, tank=exp_tank)) != 0:
        return "Tank with that user is already added"

    new_sub = TankRatingSubscription()
    new_sub.tank = exp_tank
    new_sub.wot_username = wot_username
    new_sub.user = site_username
    new_sub.save()

    update_single_tank_subscription(new_sub)

    return "Tank subscription added"


def update_single_tank_subscription(subscription: TankRatingSubscription) -> None:
    user_id = get_acc_id_by_name(subscription.wot_username)
    vehstats = get_vehicle_stats(user_id=user_id, tank_id=TankRatingSubscription.tank.tank_id)
    wn8 = calculate_wn8(
        tankId=TankRatingSubscription.tank.tank_id,
        avgDmg=vehstats['damage_per_game'],
        avgFrag=vehstats['frags_per_game'],
        avgSpot=vehstats['spotted_per_game'],
        avgDef=vehstats['def_per_game'],
        avgWinRate=vehstats['winrate'],
    )
    subscription.wn8 = wn8
    subscription.winRate = vehstats['winrate']
    subscription.dmgPerGame = vehstats['damage_per_game']
    subscription.fragPerGame = vehstats['def_per_game']
    subscription.lastUpdate = datetime.datetime.now()
    subscription.save()


def get_tank_from_name(tank_name: str) -> TankExpectations:
    exp_tank = TankExpectations.objects.filter(tank_name=tank_name)[0]
    return exp_tank


def update_wn8():
    users = {}
    subs = TankRatingSubscription.objects.all()
    for sub in subs:
        if sub.wot_username not in users.keys():
            users[sub.wot_username] = []
        users[sub.wot_username].append(sub.tank)
    for user, tanks_names in users.items():
        data = get_wn8_list(user, tanks_names)
        for tank, stats in data.items():
            tank.wn8 = stats['wn8']
            tank.lastUpdate = datetime.datetime.now()
            tank.dmgPerGame = stats['avgDmg']
            tank.fragPerGame = stats['avgFrag']
            tank.winRate = stats['avgWinRate']
            tank.spotPerGame = stats['avgSpot']
            tank.defPerGame = stats['avgDef']
            tank.save()


def get_wn8_list(player, tanks_list):
    try:
        result = {}
        pid = get_acc_id_by_name(player)
        tanks_dict_id_name = {}
        for tank_name in tanks_list:
            model = TankExpectations.objects.filter(tank_name=tank_name)[0]
            tanks_dict_id_name[model.tank_id] = tank_name
        stats = get_vehicles_stats(pid, tanks_dict_id_name.keys())
        for tank_id, vehstats in stats.items():
            tank_expectation = tanks_dict_id_name[tank_id]
            tank = TankRatingSubscription.objects.filter(tank=tank_expectation, wot_username=player)[0]
            result[tank] = get_wn8(tank_expectation, vehstats)
        return result
    except Exception as e:
        print(e)
        return -1


def calculate_wn8(tankId, avgDmg, avgSpot, avgFrag, avgDef, avgWinRate):
    expectation = TankExpectations.objects.filter(tank_id=tankId)[0]
    rDAMAGE = avgDmg / expectation.exp_Damage
    rSPOT = avgSpot / expectation.exp_Spot
    rFRAG = avgFrag / expectation.exp_Frag
    rDEF = avgDef / expectation.exp_Def
    rWIN = avgWinRate / expectation.exp_WinRate

    # step 2

    rWINc = max(0, (rWIN - 0.71) / (1 - 0.71))
    rDAMAGEc = max(0, (rDAMAGE - 0.22) / (1 - 0.22))
    rFRAGc = max(0, min(rDAMAGEc + 0.2, (rFRAG - 0.12) / (1 - 0.12)))
    rSPOTc = max(0, min(rDAMAGEc + 0.1, (rSPOT - 0.38) / (1 - 0.38)))
    rDEFc = max(0, min(rDAMAGEc + 0.1, (rDEF - 0.10) / (1 - 0.10)))

    WN8 = 980 * rDAMAGEc + 210 * rDAMAGEc * rFRAGc + 155 * rFRAGc * rSPOTc + 75 * rDEFc * rFRAGc + 145 * min(1.8, rWINc)

    return round(WN8)


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


def get_wn8(tank, vehstats):
    try:
        tank_model = TankExpectations.objects.filter(tank_name=tank)[0]

        wn8 = calculate_wn8(
            tankId=tank_model.tank_id,
            avgDmg=vehstats['damage_per_game'],
            avgFrag=vehstats['frags_per_game'],
            avgSpot=vehstats['spotted_per_game'],
            avgDef=vehstats['def_per_game'],
            avgWinRate=vehstats['winrate'],
        )

        data = {
            'wn8': wn8,
            'avgDmg': vehstats['damage_per_game'],
            'avgFrag': vehstats['frags_per_game'],
            'avgWinRate': vehstats['winrate'],
            'avgSpot': vehstats['spotted_per_game'],
            'avgDef': vehstats['def_per_game'],
            'dif_Dmg': round(vehstats['damage_per_game'] - tank_model.exp_Damage, 2),
            'dif_Frag': round(vehstats['frags_per_game'] - tank_model.exp_Frag, 2),
            'dif_expWinRate': round(vehstats['winrate'] - tank_model.exp_WinRate, 2),
        }
        return data
    except Exception as e:
        print(e)
        return -1

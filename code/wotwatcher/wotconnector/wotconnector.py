import requests


def get_acc_id(username):
    url = 'https://api.worldoftanks.eu/wot/account/list/'
    app_id = '?application_id=e71f9085bbcfb7848b6fd33ea5909f31'
    part = f'&search={username}'
    target_url = url + app_id + part
    r = requests.get(target_url)
    nickname = r.json()['data'][0]['nickname']
    acc_id = r.json()['data'][0]['account_id']
    return acc_id


def get_vehicle_stats(user_id, tank_id):
    url = f'''https://api.worldoftanks.eu/wot/tanks/stats/?application_id=e71f9085bbcfb7848b6fd33ea5909f31&account_id={user_id}+&fields=all.damage_dealt%2C+all.battles%2C+all.frags%2C+all.wins%2C+all.spotted%2C+all.dropped_capture_points&tank_id={tank_id}'''
    r = requests.get(url)
    data = r.json()['data'][f'{user_id}'][0]['all']
    data['damage_per_game'] = round(data['damage_dealt']/data['battles'], 2)
    data['frags_per_game'] = round(data['frags']/data['battles'], 2)
    data['spotted_per_game'] = round(data['spotted']/data['battles'], 2)
    data['def_per_game'] = round(data['dropped_capture_points']/data['battles'], 2)
    data['winrate'] = round((data['wins'] / data['battles'])*100, 2)

    return data

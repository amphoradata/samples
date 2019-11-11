from datetime import date
import requests
import hashlib

wz_url = "https://ws.weatherzone.com.au/" # "https://gist.githubusercontent.com/xtellurian/3ebd37c62eab565ed2efc8b4ed794fba/raw/6ab9bca400be9bbc11df54e67b3e2538f581b263/wz.json"

def load_locations(wz_user, wz_password, town, state):
    k = generate_key(wz_password)

    params = dict(
        u=wz_user,
        k=k,
        lt='aploc',
        format='json',
        latlon=1,
        ln=town,
        state=state
    )

    r = requests.get(wz_url, params=params)
    data = r.json()

    locations = data['countries'][0]['locations']
    return locations


def load_forecasts(wz_user, wz_password, wz_lc):

    k = generate_key(wz_password)

    params = dict(
        u=wz_user,
        k=k,
        lt='aploc',
        format='json',
        pdf='twc(period=168,interval=1,detail=2)',
        lc=wz_lc,
    )

    r = requests.get(wz_url, params=params)
    data = r.json()

    forecasts = data['countries'][0]['locations'][0]['part_day_forecasts']['forecasts']
    return forecasts


def make_key(day, month, year):
    return (day * 2) + (month * 300) + ( (year % 100) * 170000)

def generate_key(wz_password):
    today = date.today()
    key = make_key(today.day, today.month, today.year)
    hash = hashlib.md5()
    hash.update(f'{key}{wz_password}'.encode('utf-8'))
    k=hash.hexdigest()
    return k

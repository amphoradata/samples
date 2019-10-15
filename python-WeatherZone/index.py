import os
import amphora_client
from amphora_client import Configuration, ApiException
import requests
import hashlib
from datetime import date, datetime

# CONFIGURE
wz_user = os.environ['wz_user']
wz_password = os.environ['wz_password']
wz_lc =os.environ['wz_lc'] # location code
username=os.environ['username']
password=os.environ['password']
host=os.environ['host']
amphora_id = os.environ['amphora_id']


# EXTRACT
# download data from Weatherzone

def make_key(day, month, year):
    return (day * 2) + (month * 300) + ( (year % 100) * 170000)

today = date.today()
key = make_key(today.day, today.month, today.year)
hash = hashlib.md5()
hash.update(f'{key}{wz_password}'.encode('utf-8'))
k=hash.hexdigest()


# wz_url = "https://ws.weatherzone.com.au/"
wz_url = "https://gist.githubusercontent.com/xtellurian/3ebd37c62eab565ed2efc8b4ed794fba/raw/6ab9bca400be9bbc11df54e67b3e2538f581b263/wz.json"

# params = dict(
#     u=wz_user,
#     k=k,
#     lt='aploc',
#     format='json',
#     pdf='twc(period=168,interval=1,detail=2)',
#     lc=wz_lc
# )
params = dict()

r = requests.get(wz_url, params=params)
data = r.json()

forecasts = data['countries'][0]['locations'][0]['part_day_forecasts']['forecasts']


# TRANSFORM
now = datetime.utcnow()
signals = []
for f in forecasts: 
    signals.append(dict(
        t=f['utc_time'],
        prediction_time = now.strftime("%m/%d/%Y, %H:%M:%S"),
        temperature = f['temperature'],
        description = f['icon_phrase'],
        rain_prob = f['rain_prob']
    ))

# LOAD
configuration = Configuration(host=host)

# Create an instance of the Authentication class
auth_api = amphora_client.AuthenticationApi(amphora_client.ApiClient(configuration))
token_request = amphora_client.TokenRequest(username=username, password=password ) 

try:

    token = auth_api.api_authentication_request_post(token_request = token_request)
    configuration.api_key["Authorization"] = "Bearer " + str(token)
    client=amphora_client.ApiClient(configuration)
    # create an instance of the Users API, now with Bearer token
    users_api = amphora_client.UsersApi(client)
    me = users_api.api_users_self_get()
    print(me)

    amphora_api = amphora_client.AmphoraeApi(client)
    amphora = amphora_api.api_amphorae_id_get(amphora_id)
    print(amphora)
    c = 0
    for s in signals:
        print(f'sending signal {c}')
        signal_post = amphora_api.api_amphorae_id_signals_values_post(amphora.id, request_body=s)
        print(signal_post)
        c = c+1


except ApiException as e:
    print("Exception: %s\n" % e)

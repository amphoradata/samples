import os
import amphora_client
from amphora_client import Configuration, ApiException
from datetime import datetime
from mapping import wz_locations
from weatherzone import load_forecasts

from dotenv import load_dotenv
load_dotenv()

# CONFIGURE
wz_user = os.getenv('wz_user')
wz_password = os.getenv('wz_password')
username=os.getenv('username')
password=os.getenv('password')
host=os.getenv('host')

# this function runs a single ETL process for 1 WeatherZone location to one Amphora
def etl(wz_lc, amphora_id ):

    forecasts = load_forecasts(wz_user, wz_password, wz_lc)

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
            amphora_api.api_amphorae_id_signals_values_post(amphora.id, request_body=s)
            c = c+1


    except ApiException as e:
        print("Exception: %s\n" % e)

# for each WZ Location, run the ETL process
for wz_lc, amphora_id in wz_locations().items():
    etl(wz_lc, amphora_id)
import os

from amphora_extensions import file_uploader
import amphora_client
from amphora_client import Configuration, ApiException

from src.signals import signals
from src.weatherzone import load_forecasts, load_locations

wz_user = os.getenv('wz_user')
wz_password = os.getenv('wz_password')
host=os.getenv('host')
username=os.getenv('username')
password=os.getenv('password')

print(f'Using host: {host}')

# amphora_map == dict from wz location id to amphora id
# location_info == dict from wz location to wz location information
def create_or_update_amphorae(amphora_map, location_info):
    # LOAD
    configuration = Configuration(host=host)

    # Create an instance of the Authentication class
    auth_api = amphora_client.AuthenticationApi(amphora_client.ApiClient(configuration))
    token_request = amphora_client.TokenRequest(username=username, password=password )

    new_map = dict()
    try:
        print("Logging in")
        token = auth_api.authentication_request_token(token_request = token_request)
        configuration.api_key["Authorization"] = "Bearer " + str(token)
        print("Logged in")
        client=amphora_client.ApiClient(configuration)
        amphora_api = amphora_client.AmphoraeApi(client)
        for key in amphora_map:
            id = amphora_map[key]
            if(id == None):
                # we have to create an Amphora
                wzloc = location_info[key]
                locname = wzloc['name']
                print(f'Creating new Amphora for location {locname}')
                # create the details of the Amphora
                name = 'Weather: ' + wzloc['name'] + ' (' + wzloc['state'] + ')'
                desc = 'WeatherZone data, from ' + wzloc['name'] + '. WeatherZone code: ' + wzloc['code'] + ', PostCode: ' + wzloc['postcode']
                dto = amphora_client.CreateAmphoraDto(name=name, description=desc, price=0, lat=wzloc['latitude'], lon=wzloc['longitude'])

                res = amphora_api.amphorae_create(create_amphora_dto=dto)
                # now create the signals
                print("Creating Signals")
                for s in signals():
                    amphora_api.amphorae_create_signal(res.id, signal_dto=s)

                new_map[key] = res.id
            else:
                a = amphora_api.amphorae_read(id)
                print(f'Using existing amphora: {a.name}')
                new_map[key] = id
                existing_signals = amphora_api.amphorae_get_signals(id)
                if(len(existing_signals) > 0):
                    print('Signals exist already')
                else:
                    print('Adding signals')
                    for s in signals():
                        amphora_api.amphorae_create_signal(id, signal_dto= s)

    except ApiException as e:
        print("Error Create or update amphorae: %s\n" % e)
        raise e

    return new_map

# this function runs a single ETL process for 1 WeatherZone location to one Amphora
def upload_signals_to_amphora(wz_lc, amphora_id ):

    forecasts = load_forecasts(wz_user, wz_password, wz_lc)

    # TRANSFORM
    signals = []
    for f in forecasts:
        signals.append(dict(
            t=f['utc_time'],
            temperature = f['temperature'],
            description = f['icon_phrase'],
            rainProb = f['rain_prob'],
            windSpeed = f['wind_speed'],
            windDirection = f['wind_direction'],
            cloudCover = f['cloud_cover_percent'],
            pressure = f['pressure']
        ))

    # LOAD
    configuration = Configuration(host=host)

    # Create an instance of the Authentication class
    auth_api = amphora_client.AuthenticationApi(amphora_client.ApiClient(configuration))
    token_request = amphora_client.TokenRequest(username=username, password=password )

    try:
        print("Logging In")
        token = auth_api.authentication_request_token(token_request = token_request)
        configuration.api_key["Authorization"] = "Bearer " + str(token)
        print("Logged in")
        client=amphora_client.ApiClient(configuration)

        amphora_api = amphora_client.AmphoraeApi(client)
        amphora = amphora_api.amphorae_read(amphora_id)
        print(f'Uploading signals to {amphora.name} {amphora.id}')

        amphora_api.amphorae_upload_signal_batch(amphora.id, request_body = signals) # this sends the data to Amphora Data

        print(f'Sent {len(signals)} signals')

    except ApiException as e:
        print("Exception: %s\n" % e)
        raise e

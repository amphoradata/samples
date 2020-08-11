import os
import time
from src.signals import signals
from src.weatherzone import load_forecasts, load_locations

from amphora.client import AmphoraDataRepositoryClient

wz_user = os.getenv('wz_user')
wz_password = os.getenv('wz_password')

# amphora_map == dict from wz location id to amphora id
# location_info == dict from wz location to wz location information
def create_or_update_amphorae(client: AmphoraDataRepositoryClient, amphora_map, location_info):

    new_map = dict()
    try:
        # client=amphora_client.ApiClient(configuration)
        # amphora_api = amphora_client.AmphoraeApi(client)

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
                labels='Weather,forecast,timeseries'
                ts_cs_id='Weatherzone_Forecast'

                amphora = client.create_amphora(name, desc, price=2,
                labels=labels, lat=wzloc['latitude'], lon=wzloc['longitude'],
                    terms_and_conditions_id=ts_cs_id)

                # now create the signals
                print("Creating Signals")
                for s in signals():
                    amphora.create_signal(s._property, s.value_type, s.attributes)

                new_map[key] = amphora.id
            else:
                amphora = client.get_amphora(id)
                time.sleep(0.2) # wait a bit to prevent hitting the rate limit
                print(f'Using existing amphora: {amphora.metadata.name}')
                new_map[key] = id

    except Exception as e:
        print("Error Create or update amphorae: %s\n" % e)
        raise e

    return new_map

# this function runs a single ETL process for 1 WeatherZone location to one Amphora
def upload_signals_to_amphora(client: AmphoraDataRepositoryClient, wz_lc, amphora_id ):

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
            pressure = f['pressure'],
            rainfallRate = f['rate']
        ))

    try:
        amphora = client.get_amphora(amphora_id)
        print(f'Uploading signals to {amphora.metadata.name} {amphora.metadata.id}')
        print(f'Properties of first signal val: {signals[0].keys()}')
        amphora.push_signals_dict_array(signals) # this sends the data to Amphora Data
        print(f'Sent {len(signals)} signals')

    except Exception as e:
        print("Exception: %s\n" % e)
        raise e

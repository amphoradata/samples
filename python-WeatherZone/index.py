from dotenv import load_dotenv
load_dotenv(verbose=True)

import os
import json
from amphora.client import Credentials, AmphoraDataRepositoryClient

from src.mapping import wz_save, wz_load
from src.weatherzone import load_locations
from src.towns import towns
from src.signals import signals
from src.operations import create_or_update_amphorae, upload_signals_to_amphora

wz_user = os.getenv("wz_user")
wz_password = os.getenv('wz_password')
# amphora credentials
username=os.getenv('username')
password=os.getenv('password')
 
client = AmphoraDataRepositoryClient(Credentials(username, password))

towns = towns()
wz_locations = dict()
location_infos = dict()
# check we have all the amphora we need
for t in towns:
    locations = load_locations(wz_user, wz_password, t[0], t[1])
    store = dict()
    location_info = dict()

    for loc in locations:
        code = loc['code']
        store[code] = None
        location_info[code] = loc

    wz_locations.update(store)
    location_infos.update(location_info)

amphora_map = wz_load()
wz_locations.update(amphora_map)
print(wz_locations)

new_store = create_or_update_amphorae(client, wz_locations, location_infos)
wz_save(new_store)

# for each WZ Location, run the ETL process
for wz_lc, amphora_id in new_store.items():
    upload_signals_to_amphora(client, wz_lc, amphora_id)

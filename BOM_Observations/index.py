import logging
import sys
import os
import random
from datetime import datetime
from amphora.client import AmphoraDataRepositoryClient, Credentials

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()

import extract
import bom
import idcache
import signals
import operations as op

# provide your login credentials
credentials = Credentials(username=os.environ['username'], password=os.environ['password'])
# create a client for interacting with the public Amphora Data Repository
client = AmphoraDataRepositoryClient(credentials)


sites = extract.load_wmo_sites()

amphora_map = idcache.load()
max_t = None

# use a random amphora in the list to get the last written time.
# this should be more resilient to failure than always using the first.
if(len(amphora_map) > 0):
    random_amphora_id = random.choice(list(amphora_map.values()))
    random_amphora = client.get_amphora(random_amphora_id)
    max_t = op.get_max_t(random_amphora)
    logger.info(f'Max T is {max_t} from Amphora({random_amphora_id})')

for site in sites:
    if site.site not in amphora_map:
        logger.warn(f'Amphora doesnt exist for site {site.site}')
        # then create it
        a = op.create_amphora(client, site)
        amphora_map[site.site] = a._id
        logger.info(f'Amphora({a.amphora_id}) created for site {site.site}')
    else:
        a = client.get_amphora(amphora_map[site.site])
        logger.info(f'Amphora({a.amphora_id}) exists for site {site.site}')

    if a is not None:

        # get the max t if it doesn't exist.
        if max_t is None:
            max_t = op.get_max_t(a)

        op.ensure_signals(a)
        data = bom.get_data(site)
        if data is not None:
            op.filter_by_last_write(data, max_t)
            if len(data.observations.data) > 0:
                signal_data = signals.SignalData(data)
                a.push_signals_dict_array(signal_data.data)
                logger.info(f'Pushed {len(signal_data.data)} datums to Amphora({a.amphora_id})')
            else:
                logger.info(f'Skipping 0 length data')
        else:
            logger.warn(f'No data for Amphora({a.amphora_id}) site {site.site}')
    else: 
        logger.error(f'Lost Amphora for site {site.site}')
        raise ValueError(f'Lost Amphora for site {site.site}')

    idcache.save(amphora_map) # save on each round, so you don't lose it all

idcache.save(amphora_map)

import logging
import sys
import os
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

logger.info(f'There are {len(sites)} WMO sites')

all_data = {}
all_sites = {}

sample = bom.get_data(sites[0])
# for site in sites:
#     data = bom.get_data(site)
#     if(data is not None):
#         all_data[site.site] = data
#         all_sites[site.site] = site

# logger.info(f'Got data for {len(all_data)} sites')
# logger.info(f'Lost {len(sites) - len(all_data)} sites')

# now to create all the amphora we need, if they don't exist




amphora_map = idcache.load()

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
        op.ensure_signals(a)
        data = bom.get_data(site)
        if data is not None:
            signal_data = signals.SignalData(data)
            a.push_signals_dict_array(signal_data.data)
            logger.info(f'Pushed {len(signal_data.data)} datums to Amphora({a.amphora_id})')
        else:
            logger.warn(f'No data for Amphora({a.amphora_id}) site {site.site}')
    else: 
        logger.error(f'Lost Amphora for site {site.site}')
        raise ValueError(f'Lost Amphora for site {site.site}')

    idcache.save(amphora_map) # save on each round, so you don't lose it all
    break

idcache.save(amphora_map)

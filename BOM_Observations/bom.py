import logging
import json
import requests

import bom_types
from extract import BOMSite

logger = logging.getLogger("bom.py")


# example: http://www.bom.gov.au/fwo/IDV60801/IDV60801.95904.json
# example: http://www.bom.gov.au/fwo/IDT60803/IDT60803.89807.json
protocol = "http"
host = "www.bom.gov.au"
path= "fwo"

state_id_map = {
    "NSW": "IDN60801",
    "VIC": "IDV60801",
    "QLD": "IDQ60801",
    "WA": "IDW60801",
    "TAS": "IDT60801",
    "SA": "IDS60801",
    "NT": "IDD60801",
    "ANT": "IDT60803",
}

def construct_url(state:str, wmo: str):
    _id = state_id_map[state]
    return f'{protocol}://{host}/{path}/{_id}/{_id}.{wmo}.json'

def get_data(site: BOMSite) -> bom_types.BOMData:
    url = construct_url(site.state, site.wmo)
    res = requests.get(url)
    logger.info(f'{url} returned {res.status_code}')
    try:    
        data = res.json()
        return bom_types.bom_data_from_dict(data)
    except AssertionError as assErr:
        raise assErr
    except:
        logger.error(f'{res.status_code} {site.source} {site.name} {site.state}, {url}')
        return None

# Darwin airport letter is actually D - so IDD
import logging
logger = logging.getLogger("operations.py")
from datetime import datetime, timedelta
from amphora.client import AmphoraDataRepositoryClient, Amphora
from amphora_api_client import DateTimeRange
import pytz

import signals
from extract import BOMSite
from bom_types import BOMData

TERMS_ID = "Creative_Commons_3_AU"
PRICE = 2
labels = ["weather", "observations"]

def create_amphora(client: AmphoraDataRepositoryClient, site: BOMSite)-> Amphora:
    return client.create_amphora(f'Weather Observations: {site.name}, {site.state}', des(site),
        price=PRICE, lat=site.lat, lon=site.lon, terms_and_conditions_id=TERMS_ID, labels=labels )

def ensure_signals(amphora: Amphora):
    required_signals = signals.required_signals()
    actual_signals = amphora.get_signals()
    if(len(required_signals) > len(actual_signals.metadata)):
        # then we need to add some signals
        for s in required_signals:
            if not contains_signal(amphora,s._property):
                logger.warn(f'Adding signal {s._property} to Amphora({amphora.amphora_id})')
                amphora.create_signal(s._property, value_type="Numeric", attributes= s.attributes)

def des(site: BOMSite) -> str:
    f = open("description.md")
    s = f.read()
    s = s.replace("{{NAME}}", site.name).replace("{{STATE}}", site.state).replace("{{STATE}}", site.state)
    s = s.replace("{{SITE}}", site.site).replace("{{HEIGHT}}", str(site.height)).replace("{{BAR_HT}}", str(site.bar_ht))
    return s

def contains_signal(amphora: Amphora, _property: str) -> bool:
    signals = amphora.get_signals()
    for s in signals.metadata:
        if s._property == _property:
            return True
    return False

def get_max_t(amphora: Amphora):
    _from = datetime.utcnow() + timedelta(days=-3)
    dtrange = DateTimeRange(_from=_from, to=datetime.utcnow())
    df = amphora.get_signals().pull(dtrange).to_pandas()
    if len(df.index) > 0:
        max_t = df.index.max()
    else:
        max_t = _from

    logger.info(f'Max T is {max_t} UTC')
    return max_t.replace(tzinfo= pytz.UTC)

def filter_by_last_write(data: BOMData, max_t: datetime) -> BOMData:
    filtered = []
    count_removed = 0
    for datum in data.observations.data:
        if signals.get_timestamp(datum.aifstime_utc) > max_t:
            filtered.append(datum)
        else:
            count_removed = count_removed + 1

    logger.info(f'Removed {count_removed} datum, there are {len(filtered)} remaining')
    data.observations.data = filtered
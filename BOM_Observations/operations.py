import logging
logger = logging.getLogger("operations.py")
from amphora.client import AmphoraDataRepositoryClient, Amphora
from extract import BOMSite
import signals

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
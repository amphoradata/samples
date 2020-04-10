from logging import getLogger
logger = getLogger("extract.py")
# functions

def select_and_strip(line: str, start: int, end: int) -> [str]:
    return line[start:end - 1].strip()

def float_or_none(s: str) -> float:
    try:
        return float(s)
    except ValueError:
        return None

def int_or_none(s: str) -> int:
    try:
        return int(s)
    except ValueError:
        return None

class BOMSite():
    def __init__(self, site: str, 
                    dist:str, 
                    name:str, 
                    start_year:int, 
                    end_year:int, 
                    lat:float, 
                    lon:float, 
                    source:str, 
                    state:str, 
                    height:float,
                    bar_ht:float, 
                    wmo:float):
        self.site = site
        self.dist = dist
        self.name = name
        self.start_year = int_or_none(start_year)
        self.end_year = int_or_none(end_year)
        self.lat = float_or_none(lat)
        self.lon = float_or_none(lon)
        self.source = source
        self.state = state
        self.height = float_or_none(height)
        self.bar_ht = float_or_none(bar_ht)
        self.wmo = int_or_none(wmo)
    
    def __str__(self):
        return f'{self.site}, {self.name} {self.state}, WMO: {self.wmo} '

def to_site(line:str, indexes:[int]) -> BOMSite:
    v = []
    for i in range(len(indexes) - 1):
        value = select_and_strip(line, indexes[i], indexes[i+1])
        v.append(value)

    if(len(v) != 12):
        logger.error(v)
        raise ValueError("Incorrect Length")
    return BOMSite(v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7], v[8], v[9], v[10], v[11])


def remove_without_wmo(sites: [BOMSite]) -> [BOMSite]:
    res = []
    for s in sites: 
        if s.wmo != None : 
            res.append(s)
    return res

def remove_ended(sites: [BOMSite]) -> [BOMSite]:
    res = []
    for s in sites: 
        if s.end_year is None: 
            res.append(s)
    return res


def load_wmo_sites()-> [BOMSite]:

    f = open("stations.txt", "r")
    # we are going to discard the first 4 lines
    lines = f.readlines()
    dashline = lines[3]
    last_index = 0
    indexes = []
    for dashes in dashline.split(' '):
        indexes.append(last_index)
        last_index = len(dashes) + last_index + 1

    indexes.append(len(dashline))
    lines = lines[4:]

    sites = []
    for line in lines:
        sites.append(to_site(line, indexes))

    logger.info(f'There are {len(sites)} sites')
    wmo_sites = remove_without_wmo(sites)
    logger.info(f'There are {len(wmo_sites)} WMO sites')
    current_wmo_sites = remove_ended(wmo_sites)
    logger.info(f'There are {len(current_wmo_sites)} current WMO sites')
    return current_wmo_sites

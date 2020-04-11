import datetime
import pytz
from bom_types import BOMData

air_temp = "airTemp"
apparent_temp = "apparentTemp"
cloud= "cloud"
dew_point = "dewPoint"
pressure = "pressure"
rain_trace = "rainTrace"
relatice_humidity = "relativeHumidity"
wind_speed= "windSpeed"

class SignalData():
    def __init__(self, data: BOMData):
        result = []
        for datum in data.observations.data:
            result.append({
                "t": get_timestamp(datum.aifstime_utc),
                air_temp: datum.air_temp,
                apparent_temp: datum.apparent_t,
                cloud: datum.cloud_oktas,
                dew_point: datum.dewpt,
                pressure: datum.press,
                rain_trace: to_float(datum.rain_trace),
                relatice_humidity: datum.rel_hum,
                wind_speed: datum.wind_spd_kmh
            })
        self.data = result    

class SignalDefinition():
    def __init__(self, _property:str, units: str):
        self._property = _property
        self.value_type="Numeric"
        self.attributes = {"units": units}


def required_signals()-> [SignalDefinition]:
    return [
        SignalDefinition(air_temp, "c"),
        SignalDefinition(apparent_temp, "c"),
        SignalDefinition(cloud, "oktas"),
        SignalDefinition(dew_point, "c"),
        SignalDefinition(pressure, "hPa"),
        SignalDefinition(rain_trace, "mm"),
        SignalDefinition(relatice_humidity, "c"),
        SignalDefinition(wind_speed, "km/h"),
    ]

def get_timestamp(aifstime_utc: str):
    return datetime.datetime.strptime(aifstime_utc, "%Y%m%d%H%M%S").replace(tzinfo=pytz.UTC)


def to_float(x):
    try:
        return float(x)
    except:
        return None

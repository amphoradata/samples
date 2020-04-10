# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = bom_data_from_dict(json.loads(json_string))

from enum import Enum
from typing import Any, List, TypeVar, Type, Callable, cast


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class Datum:
    sort_order: int
    wmo: int
    name: str
    history_product: str
    local_date_time: str
    local_date_time_full: str
    aifstime_utc: str
    lat: float
    lon: float
    apparent_t: float
    cloud: str
    cloud_base_m: str
    cloud_oktas: int
    cloud_type: str
    cloud_type_id: str
    delta_t: float
    gust_kmh: int
    gust_kt: int
    air_temp: float
    dewpt: float
    press: float
    press_msl: float
    press_qnh: float
    press_tend: str
    rain_trace: str
    rel_hum: int
    sea_state: str
    swell_dir_worded: str
    swell_height: float
    swell_period: float
    vis_km: str
    weather: str
    wind_dir: str
    wind_spd_kmh: int
    wind_spd_kt: int

    def __init__(self, sort_order: int, wmo: int, name: str, history_product: str, local_date_time: str, local_date_time_full: str, aifstime_utc: str, lat: float, lon: float, apparent_t: float, cloud: str, cloud_base_m: None, cloud_oktas: int, cloud_type: str, cloud_type_id: None, delta_t: float, gust_kmh: int, gust_kt: int, air_temp: float, dewpt: float, press: float, press_msl: float, press_qnh: float, press_tend: str, rain_trace: str, rel_hum: int, sea_state: str, swell_dir_worded: str, swell_height: None, swell_period: None, vis_km: str, weather: str, wind_dir: str, wind_spd_kmh: int, wind_spd_kt: int) -> None:
        self.sort_order = sort_order
        self.wmo = wmo
        self.name = name
        self.history_product = history_product
        self.local_date_time = local_date_time
        self.local_date_time_full = local_date_time_full
        self.aifstime_utc = aifstime_utc
        self.lat = lat
        self.lon = lon
        self.apparent_t = apparent_t
        self.cloud = cloud
        self.cloud_base_m = cloud_base_m
        self.cloud_oktas = cloud_oktas
        self.cloud_type = cloud_type
        self.cloud_type_id = cloud_type_id
        self.delta_t = delta_t
        self.gust_kmh = gust_kmh
        self.gust_kt = gust_kt
        self.air_temp = air_temp
        self.dewpt = dewpt
        self.press = press
        self.press_msl = press_msl
        self.press_qnh = press_qnh
        self.press_tend = press_tend
        self.rain_trace = rain_trace
        self.rel_hum = rel_hum
        self.sea_state = sea_state
        self.swell_dir_worded = swell_dir_worded
        self.swell_height = swell_height
        self.swell_period = swell_period
        self.vis_km = vis_km
        self.weather = weather
        self.wind_dir = wind_dir
        self.wind_spd_kmh = wind_spd_kmh
        self.wind_spd_kt = wind_spd_kt

    @staticmethod
    def from_dict(obj: Any) -> 'Datum':
        assert isinstance(obj, dict)
        sort_order = from_int(obj.get("sort_order"))
        wmo = from_int(obj.get("wmo"))
        name = from_str(obj.get("name"))
        history_product = from_str(obj.get("history_product"))
        local_date_time = from_str(obj.get("local_date_time"))
        local_date_time_full = from_str(obj.get("local_date_time_full"))
        aifstime_utc = from_str(obj.get("aifstime_utc"))
        lat = from_float(obj.get("lat"))
        lon = from_float(obj.get("lon"))
        apparent_t = from_union( [from_float, from_none] ,obj.get("apparent_t"))
        cloud = from_str(obj.get("cloud"))
        cloud_base_m = from_union([from_none, from_int], obj.get("cloud_base_m"))
        cloud_oktas = from_union([from_int, from_none], obj.get("cloud_oktas"))
        cloud_type = from_str(obj.get("cloud_type"))
        cloud_type_id = from_union([from_none, from_float], obj.get("cloud_type_id"))
        delta_t = from_union( [from_float, from_none], obj.get("delta_t"))
        gust_kmh = from_union([from_int, from_none] ,obj.get("gust_kmh"))
        gust_kt = from_union( [from_int, from_none], obj.get("gust_kt"))
        air_temp = from_union( [from_float, from_none], obj.get("air_temp"))
        dewpt = from_union([from_float, from_none],obj.get("dewpt"))
        press = from_union([from_float, from_none], obj.get("press"))
        press_msl = from_union([from_float, from_none], obj.get("press_msl"))
        press_qnh = from_union( [from_float, from_none] ,obj.get("press_qnh"))
        press_tend = from_str(obj.get("press_tend"))
        rain_trace = from_str(obj.get("rain_trace"))
        rel_hum = from_union([from_int, from_none], obj.get("rel_hum"))
        sea_state = from_str(obj.get("sea_state"))
        swell_dir_worded = from_str(obj.get("swell_dir_worded"))
        swell_height = from_union([from_none, from_float], obj.get("swell_height"))
        swell_period = from_union([from_none, from_float], obj.get("swell_period"))
        vis_km = from_str(obj.get("vis_km"))
        weather = from_str(obj.get("weather"))
        wind_dir = from_str(obj.get("wind_dir"))
        wind_spd_kmh = from_union( [from_int, from_none],obj.get("wind_spd_kmh"))
        wind_spd_kt = from_union( [from_int, from_none] ,obj.get("wind_spd_kt"))
        return Datum(sort_order, wmo, name, history_product, local_date_time, local_date_time_full, aifstime_utc, lat, lon, apparent_t, cloud, cloud_base_m, cloud_oktas, cloud_type, cloud_type_id, delta_t, gust_kmh, gust_kt, air_temp, dewpt, press, press_msl, press_qnh, press_tend, rain_trace, rel_hum, sea_state, swell_dir_worded, swell_height, swell_period, vis_km, weather, wind_dir, wind_spd_kmh, wind_spd_kt)

    def to_dict(self) -> dict:
        result: dict = {}
        result["sort_order"] = from_int(self.sort_order)
        result["wmo"] = from_int(self.wmo)
        result["name"] = from_str(self.name)
        result["history_product"] = from_str(self.history_product)
        result["local_date_time"] = from_str(self.local_date_time)
        result["local_date_time_full"] = from_str(self.local_date_time_full)
        result["aifstime_utc"] = from_str(self.aifstime_utc)
        result["lat"] = to_float(self.lat)
        result["lon"] = to_float(self.lon)
        result["apparent_t"] = to_float(self.apparent_t)
        result["cloud"] = from_str(self.cloud)
        result["cloud_base_m"] = from_union([from_none, from_float], self.cloud_base_m)
        result["cloud_oktas"] = from_union([from_int, from_none], self.cloud_oktas)
        result["cloud_type"] = from_str(self.cloud_type)
        result["cloud_type_id"] = from_union([from_none, from_str], self.cloud_type_id)
        result["delta_t"] = to_float(self.delta_t)
        result["gust_kmh"] = from_int(self.gust_kmh)
        result["gust_kt"] = from_int(self.gust_kt)
        result["air_temp"] = to_float(self.air_temp)
        result["dewpt"] = to_float(self.dewpt)
        result["press"] = to_float(self.press)
        result["press_msl"] = to_float(self.press_msl)
        result["press_qnh"] = to_float(self.press_qnh)
        result["press_tend"] = from_str(self.press_tend)
        result["rain_trace"] = from_str(self.rain_trace)
        result["rel_hum"] = from_int(self.rel_hum)
        result["sea_state"] = from_str(self.sea_state)
        result["swell_dir_worded"] = from_str(self.swell_dir_worded)
        result["swell_height"] = from_union([from_none, from_float], self.swell_height)
        result["swell_period"] = from_union([from_none, from_float], self.swell_period)
        result["vis_km"] = from_str(self.vis_km)
        result["weather"] = from_str(self.weather)
        result["wind_dir"] = from_str(self.wind_dir)
        result["wind_spd_kmh"] = from_int(self.wind_spd_kmh)
        result["wind_spd_kt"] = from_int(self.wind_spd_kt)
        return result


class Header:
    refresh_message: str
    id: str
    main_id: str
    name: str
    state_time_zone: str
    time_zone: str
    product_name: str
    state: str

    def __init__(self, refresh_message: str, id: str, main_id: str, name: str, state_time_zone: str, time_zone: str, product_name: str, state: str) -> None:
        self.refresh_message = refresh_message
        self.id = id
        self.main_id = main_id
        self.name = name
        self.state_time_zone = state_time_zone
        self.time_zone = time_zone
        self.product_name = product_name
        self.state = state

    @staticmethod
    def from_dict(obj: Any) -> 'Header':
        assert isinstance(obj, dict)
        refresh_message = from_str(obj.get("refresh_message"))
        id = from_str(obj.get("ID"))
        main_id = from_str(obj.get("main_ID"))
        name = from_str(obj.get("name"))
        state_time_zone = from_str(obj.get("state_time_zone"))
        time_zone = from_str(obj.get("time_zone"))
        product_name = from_str(obj.get("product_name"))
        state = from_str(obj.get("state"))
        return Header(refresh_message, id, main_id, name, state_time_zone, time_zone, product_name, state)

    def to_dict(self) -> dict:
        result: dict = {}
        result["refresh_message"] = from_str(self.refresh_message)
        result["ID"] = from_str(self.id)
        result["main_ID"] = from_str(self.main_id)
        result["name"] = from_str(self.name)
        result["state_time_zone"] = from_str(self.state_time_zone)
        result["time_zone"] = from_str(self.time_zone)
        result["product_name"] = from_str(self.product_name)
        result["state"] = from_str(self.state)
        return result


class Notice:
    copyright: str
    copyright_url: str
    disclaimer_url: str
    feedback_url: str

    def __init__(self, copyright: str, copyright_url: str, disclaimer_url: str, feedback_url: str) -> None:
        self.copyright = copyright
        self.copyright_url = copyright_url
        self.disclaimer_url = disclaimer_url
        self.feedback_url = feedback_url

    @staticmethod
    def from_dict(obj: Any) -> 'Notice':
        assert isinstance(obj, dict)
        copyright = from_str(obj.get("copyright"))
        copyright_url = from_str(obj.get("copyright_url"))
        disclaimer_url = from_str(obj.get("disclaimer_url"))
        feedback_url = from_str(obj.get("feedback_url"))
        return Notice(copyright, copyright_url, disclaimer_url, feedback_url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["copyright"] = from_str(self.copyright)
        result["copyright_url"] = from_str(self.copyright_url)
        result["disclaimer_url"] = from_str(self.disclaimer_url)
        result["feedback_url"] = from_str(self.feedback_url)
        return result


class Observations:
    notice: List[Notice]
    header: List[Header]
    data: List[Datum]

    def __init__(self, notice: List[Notice], header: List[Header], data: List[Datum]) -> None:
        self.notice = notice
        self.header = header
        self.data = data

    @staticmethod
    def from_dict(obj: Any) -> 'Observations':
        assert isinstance(obj, dict)
        notice = from_list(Notice.from_dict, obj.get("notice"))
        header = from_list(Header.from_dict, obj.get("header"))
        data = from_list(Datum.from_dict, obj.get("data"))
        return Observations(notice, header, data)

    def to_dict(self) -> dict:
        result: dict = {}
        result["notice"] = from_list(lambda x: to_class(Notice, x), self.notice)
        result["header"] = from_list(lambda x: to_class(Header, x), self.header)
        result["data"] = from_list(lambda x: to_class(Datum, x), self.data)
        return result


class BOMData:
    observations: Observations

    def __init__(self, observations: Observations) -> None:
        self.observations = observations

    @staticmethod
    def from_dict(obj: Any) -> 'BOMData':
        assert isinstance(obj, dict)
        observations = Observations.from_dict(obj.get("observations"))
        return BOMData(observations)

    def to_dict(self) -> dict:
        result: dict = {}
        result["observations"] = to_class(Observations, self.observations)
        return result


def bom_data_from_dict(s: Any) -> BOMData:
    return BOMData.from_dict(s)


def bom_data_to_dict(x: BOMData) -> Any:
    return to_class(BOMData, x)

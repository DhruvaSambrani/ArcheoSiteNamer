import json
_JSON_DATA = json.load(open("res/zonemaping.json"))
_MAJOR_WIDTH = _JSON_DATA["majorWidth"]
_MINOR_WIDTH = _JSON_DATA["minorWidth"]
_START_LNG = _JSON_DATA["startLng"]
_END_LAT = _JSON_DATA["endLat"]
_MAJOR_ZONES = {}
for key in _JSON_DATA["majorZones"].keys():
    _MAJOR_ZONES[tuple(int(i) for i in key.split(","))
                 ] = _JSON_DATA["majorZones"][key]
_MINOR_ZONES = {}
for key in _JSON_DATA["minorZones"].keys():
    _MINOR_ZONES[tuple(int(i) for i in key.split(","))
                 ] = _JSON_DATA["minorZones"][key]
del _JSON_DATA


class InvalidLocationError(Exception):
    pass


def get_major_zone(lat, lng):
    if _END_LAT < lat or lng < _START_LNG:
        raise InvalidLocationError("No zone here")
    row = (_END_LAT - lat) // _MAJOR_WIDTH
    col = (lng - _START_LNG) // _MAJOR_WIDTH
    try:
        major = _MAJOR_ZONES[(row, col)]
        return major
    except KeyError:
        raise InvalidLocationError("No zone here")


def get_minor_zone(lat, lng):
    row = ((_END_LAT - lat) % _MAJOR_WIDTH) // _MINOR_WIDTH
    column = ((lng - _START_LNG) % _MAJOR_WIDTH) // _MINOR_WIDTH
    return _MINOR_ZONES[(row, column)]

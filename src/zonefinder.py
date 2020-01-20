import json
_json_data = json.load(open("res/zonemaping.json"))
_major_width = _json_data["majorWidth"]
_minor_width = _json_data["minorWidth"]
_start_lng = _json_data["startLng"]
_end_lat = _json_data["endLat"]
_major_zones = {}
for key in _json_data["majorZones"].keys():
    _major_zones[tuple(int(i) for i in key.split(","))
                 ] = _json_data["majorZones"][key]
_minorZones = {}
for key in _json_data["minorZones"].keys():
    _minorZones[tuple(int(i) for i in key.split(","))
                ] = _json_data["minorZones"][key]
del _json_data


class InvalidLocationError(Exception):
    pass


def get_major_zone(lat, lng):
    if _end_lat < lat or lng < _start_lng:
        raise InvalidLocationError("No zone here")
    row = (_end_lat - lat) // _major_width
    col = (lng - _start_lng) // _major_width
    try:
        major = _major_zones[(row, col)]
        return major
    except KeyError:
        raise InvalidLocationError("No zone here")


def get_minor_zone(lat, lng):
    row = ((_end_lat - lat) % _major_width) // _minor_width
    column = ((lng - _start_lng) % _major_width) // _minor_width
    return _minorZones[(row, column)]

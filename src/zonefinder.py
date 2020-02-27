import json
import sys
import os
try:
    _WD = sys._MEIPASS  # skipcq: PYL-W0212
except AttributeError:
    _WD = os.path.dirname(__file__)
_JSON_DATA = json.load(open(os.path.join(_WD, "res/zonemapping.json")))
_MAJOR_WIDTH = _JSON_DATA["majorWidth"]
_MINOR_WIDTH = _JSON_DATA["minorWidth"]
_START_LNG = _JSON_DATA["startLng"]
_END_LAT = _JSON_DATA["endLat"]
_MAJOR_ZONES = {}
for key in _JSON_DATA["major_zones"].keys():
    _MAJOR_ZONES[tuple(int(i) for i in key.split(","))
                 ] = _JSON_DATA["major_zones"][key]
_MINOR_ZONES = {}
for key in _JSON_DATA["minor_zones"].keys():
    _MINOR_ZONES[
        tuple(int(i) for i in key.split(","))] = _JSON_DATA["minor_zones"][key]
del _JSON_DATA


class InvalidLocationError(Exception):
    """Raised when location does not exist in a zone"""


def get_major_zone(lat, lng):
    """Get the major zone, given the latitude and longitude"""
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
    """Get the minor zone, given the latitude and longitude"""
    row = ((_END_LAT - lat) % _MAJOR_WIDTH) // _MINOR_WIDTH
    column = ((lng - _START_LNG) % _MAJOR_WIDTH) // _MINOR_WIDTH
    return _MINOR_ZONES[(row, column)]

import json
jsonData = json.load(open("res/zonemaping.json"))
_majorWidth = jsonData["majorWidth"]
_minorWidth = jsonData["minorWidth"]
_startLng = jsonData["startLng"]
_endLat = jsonData["endLat"]
_majorZones = {}
for key in jsonData["majorZones"].keys():
    _majorZones[tuple(int(i) for i in key.split(","))] = jsonData["majorZones"][key]
_minorZones = {}
for key in jsonData["minorZones"].keys():
    _minorZones[tuple(int(i) for i in key.split(","))] = jsonData["minorZones"][key]
del jsonData

class InvalidLocationError(Exception):
    pass

def getMajorZone(lat, lng):
    if _endLat<lat or lng<_startLng:
        raise InvalidLocationError("No zone here")
    row = (_endLat - lat) // _majorWidth
    col = (lng - _startLng) // _majorWidth
    try:
        major = _majorZones[(row,col)]
        return major
    except (KeyError):
        raise InvalidLocationError("No zone here")

def getMinorZone(lat, lng):
    row = ((_endLat - lat) % _majorWidth) // _minorWidth
    column = ((lng - _startLng) % _majorWidth) // _minorWidth
    return _minorZones[(row,column)]

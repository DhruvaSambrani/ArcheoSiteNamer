import sqlite3
from settings import settings
from os.path import expanduser as homepath

_CONN = sqlite3.connect(homepath('~/.ArcheoSiteNamer/database.db'))
_CURSOR = _CONN.cursor()

HEADERS = [
    "Site Name",
    "Site Code",
    "Site Description",
    "Researcher",
    "Old Code"]
_ATTRMAP = {
    "majorZone": 0,
    "minorZone": 1,
    "latitude": 2,
    "longitude": 3,
    "name": 4,
    "abbr": 5,
    "description": 6,
    "researcher": 7,
    "oldcode": 8}


def _create_table():
    _CURSOR.execute('''
    CREATE TABLE IF NOT EXISTS "mainTable" (
        "majorZone" TEXT NOT NULL,
        "minorZone" TEXT NOT NULL,
        "latitude" NUMBER NOT NULL,
        "longitude" NUMBER NOT NULL,
        "name" TEXT NOT NULL,
        "abbr" TEXT NOT NULL,
        "description" TEXT,
        "researcher" TEXT NOT NULL,
        "oldcode" TEXT,
        PRIMARY KEY("majorZone", "minorZone", "abbr"),
        UNIQUE("majorZone", "minorZone", "abbr")
    )
    ''')
    return _CURSOR


def fetch_by_id(major, minor, abbr):
    return [format_row(row) for row in _CURSOR.execute(
        f"SELECT * FROM mainTable WHERE majorZone = '{major}' AND "
        f"minorZone = '{minor}' AND abbr = '{abbr}'")]


def fetch_by_researcher(researcher):
    return [format_row(row) for row in _CURSOR.execute(
        f"SELECT * FROM mainTable WHERE researcher = '{researcher}'")]


def fetch_all():
    return [format_row(row)
            for row in _CURSOR.execute("SELECT * FROM mainTable")]


def format_row(row):
    temp = []
    temp.append(row[_ATTRMAP["name"]])
    temp.append(row[_ATTRMAP["majorZone"]] +
                row[_ATTRMAP["minorZone"]] +
                row[_ATTRMAP["abbr"]])
    temp.append(row[_ATTRMAP["description"]][:settings.getint(
        "desc_length")] + (row[4][settings.getint("desc_length"):] and '...'))
    temp.append(row[_ATTRMAP["researcher"]])
    temp.append(row[_ATTRMAP["oldcode"]])
    return temp


def execute_sql(s):
    _CURSOR.execute(s)


def insert(majorZone, minorZone, latitude, longitude,
           name, abbr, description, researcher, oldcode):
    """
    Inserts values into db.
    Parameters
    ----------
    majorZone
    minorZone
    latitude
    longitude
    name
    abbr
    description
    researcher
    oldcode
    """
    _CURSOR.execute(
        "INSERT INTO mainTable VALUES (?,?,?,?,?,?,?,?,?)",
        (majorZone,
         minorZone,
         latitude,
         longitude,
         name,
         abbr,
         description,
         researcher,
         oldcode))


def delete_all():
    _CURSOR.execute('''DELETE FROM "mainTable"''')


def commit_changes():
    _CONN.commit()


def cleanup():
    _CONN.commit()
    _CONN.close()

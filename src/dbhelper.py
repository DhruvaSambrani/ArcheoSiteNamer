import sqlite3
from settings import settings
from os.path import expanduser as homepath

conn = sqlite3.connect(homepath('~/.ArcheoSiteNamer/database.db'))
c = conn.cursor()

headers=["Site Name", "Site Code", "Site Description", "Researcher", "Old Code"]
_attrmap = {
    "majorZone":0,
    "minorZone":1,
    "latitude":2,
    "longitude":3,
    "name":4,
    "abbr":5,
    "description":6,
    "researcher":7,
    "oldcode":8 }
def createTable():
    c.execute('''
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
    return c

def fetchByID(major, minor, abbr):
    return [formatRow(row) for row in c.execute(f"SELECT * FROM mainTable WHERE majorZone = '{major}' AND minorZone = '{minor}' AND abbr = '{abbr}'")]

def fetchByResearcher(researcher):
    return [formatRow(row) for row in c.execute(f"SELECT * FROM mainTable WHERE researcher = '{researcher}'")]

def fetchAll():
    return [formatRow(row) for row in c.execute("SELECT * FROM mainTable")]

def formatRow(row):
    temp = []
    temp.append(row[_attrmap["name"]])
    temp.append(row[_attrmap["majorZone"]]+row[_attrmap["minorZone"]]+row[_attrmap["abbr"]])
    temp.append(row[_attrmap["description"]][:settings.getint("desc_length")] + (row[4][settings.getint("desc_length"):] and '...'))
    temp.append(row[_attrmap["researcher"]])
    temp.append(row[_attrmap["oldcode"]])
    return temp

def executeSQL(s):
    c.execute(s)

def insert(majorZone, minorZone, latitude, longitude, name, abbr, description, researcher, oldcode):
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
    c.execute("INSERT INTO mainTable VALUES (?,?,?,?,?,?,?,?,?)", (majorZone, minorZone, latitude, longitude, name, abbr, description, researcher, oldcode))

def deleteAll():
    c.execute('''DELETE FROM "mainTable"''')

def commitChanges():
    conn.commit()
def cleanup():
    conn.commit()
    conn.close()

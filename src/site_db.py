"""
Database for Sites.
Table Name
----------
siteTable

Fields
------
Site: Class
fetch_by_id()
fetch_all()
fetch_by_sql()
"""
import pprsite_map
from dbhelper import execute_sql, init_db
init_db()


class Site:
    pass

HEADERS = [
    "Major Zone",
    "Minor Zone",
    "Latitude",
    "Longitude",
    "Code",
    "Name",
    "Description",
    "Old Code"]
_ATTRMAP = {
    "majorZone": 0,
    "minorZone": 1,
    "latitude": 2,
    "longitude": 3,
    "abbr": 4,
    "name": 5,
    "description": 6,
    "oldcode": 7}


class Site:
    """ The Site object is a python representation
of the entry held in the database.
    Fields
    ------
        major_zone
        minor_zone
        latitude
        longitude
        name
        abbr
        description
        oldcode

    Functions
    ---------
        __init__(self, row: iterable)
        __str__(self)
        insert(self)
        delete(self)
"""
    majorZone: str
    minorZone: str
    latitude: float
    longitude: float
    abbr: str
    name: str
    oldcode: str
    description: str

    def __init__(self, row):
        """ Constructor
Params
------
self: Site
row: iterable
    iterable indexed according _ATTRMAP
"""
        self.majorZone = row[_ATTRMAP["majorZone"]]
        self.minorZone = row[_ATTRMAP["minorZone"]]
        self.latitude = float(row[_ATTRMAP["latitude"]])
        self.longitude = float(row[_ATTRMAP["longitude"]])
        self.abbr = row[_ATTRMAP["abbr"]]
        self.name = row[_ATTRMAP["name"]]
        self.description = row[_ATTRMAP["description"]]
        self.oldcode = row[_ATTRMAP["oldcode"]]

    def __str__(self, desc_length=20):
        temp = {}
        temp["Name"] = self.name
        temp["ID"] = self.majorZone +\
            self.minorZone +\
            self.abbr
        temp["Longitude"] = self.longitude
        temp["Latitude"] = self.latitude
        temp["Description"] = self.description[:desc_length] +\
            (self.description[desc_length:] and '...')
        temp["Old Code"] = self.oldcode
        return temp.__str__()

    def fetch_papers(self):
        return pprsite_map.fetch_paper_by_site(self.get_id())

    def get_id(self):
        return self.majorZone + self.minorZone + self.abbr

    def insert(self):
        """ Inserts self into db."""
        execute_sql(
            "INSERT INTO siteTable VALUES (?,?,?,?,?,?,?,?)",
            (self.majorZone,
             self.minorZone,
             self.latitude,
             self.longitude,
             self.abbr,
             self.name,
             self.description,
             self.oldcode))

    def delete(self):
        """Deletes self from db."""
        execute_sql(
            f'''
            DELETE FROM "siteTable"
            where majorZone = '{self.majorZone}' AND
            minorZone = '{self.minorZone}' AND
            abbr = '{self.abbr}' '''
        )


def _create_table():
    execute_sql('''
    CREATE TABLE IF NOT EXISTS "siteTable" (
        "majorZone" TEXT NOT NULL,
        "minorZone" TEXT NOT NULL,
        "latitude" NUMBER NOT NULL,
        "longitude" NUMBER NOT NULL,
        "abbr" TEXT NOT NULL,
        "name" TEXT NOT NULL,
        "description" TEXT,
        "oldcode" TEXT,
        PRIMARY KEY("majorZone", "minorZone", "abbr"),
        UNIQUE("majorZone", "minorZone", "abbr")
    )
    ''')


def fetch_all():
    """Return a list of all sites"""
    return [Site(row) for row in execute_sql("SELECT * FROM siteTable")]


def fetch_by_id(major, minor, abbr):
    """Fetch the site by id
Params
------
major: String
    The major zone of the site
minor: String
    The minor zone of the site
abbr: String
    The abbr code of the site
"""
    return Site(execute_sql(
        f"SELECT * FROM siteTable WHERE majorZone = '{major}' AND "
        f"minorZone = '{minor}' AND abbr = '{abbr}'").fetchone())


def fetch_by_sql(clause, param):
    """Fetch sites by query
clause: String
    Contains the clause for the query. SELECT will be added automatically.
    eg: "WHERE name='?'"
params: Tuple = ()
    Arguments to add to clause
"""
    query = '''SELECT * from siteTable ''' + clause
    return [Site(row) for row in execute_sql(query, param)]


_create_table()

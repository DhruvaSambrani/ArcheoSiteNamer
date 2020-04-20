"""
Database for Papers.
Table Name
----------
paperTable

Fields
------
Paper: Class
fetch_all()
fetch_by_doi()
fetch_by_sql()
"""

from ArcheoSiteNamer.dbhelper import execute_sql


class Paper:
    pass


import ArcheoSiteNamer.pprsite_map as pprsite_map

HEADERS = [
    "Title",
    "DOI",
    "Description",
    "URL"]

_ATTRMAP = {
    "title": 0,
    "doi": 1,
    "description": 2,
    "url": 3}


class Paper:
    """ The Paper object is a python representation
of the entry held in the database.
    Fields
    ----------
        title : str
        doi : str :: PRIMARY KEY
        description : str
        url : str
    Functions
    ---------
        __init__(self, row: iterable)
        __str__(self)
        insert(self)
        delete(self)
    """
    title: str
    doi: str
    description: str
    url: str

    def __init__(self, row):
        """ Constructor
Params
------
self: Paper
row: iterable
    iterable indexed according _ATTRMAP
"""
        self.title = row[_ATTRMAP["title"]]
        self.description = row[_ATTRMAP["description"]]
        self.doi = row[_ATTRMAP["doi"]]
        self.url = row[_ATTRMAP["url"]]

    def __str__(self, desc_length=20):
        temp = {}
        temp["Title"] = self.title
        temp["DOI"] = self.doi
        temp["URL"] = self.url
        temp["Description"] = self.description[:desc_length] +\
            (self.description[desc_length:] and '...')
        return temp.__str__()

    def insert(self):
        """ Inserts self into db."""
        execute_sql(
            "INSERT INTO paperTable VALUES (?,?,?,?)", (
                self.title,
                self.doi,
                self.description,
                self.url
            )
        )

    def delete(self):
        """Deletes self from db."""
        execute_sql(
            f'''
            DELETE FROM "paperTable"
            where doi = '{self.doi}'
            '''
        )

    def fetch_sites(self):
        return pprsite_map.fetch_paper_by_site(self.get_id())


def _create_table():
    execute_sql('''
    CREATE TABLE IF NOT EXISTS "paperTable" (
        "title" TEXT NOT NULL,
        "doi" TEXT NOT NULL,
        "description" TEXT,
        "url" TEXT,
        PRIMARY KEY("doi"),
        UNIQUE("doi")
    )
    ''')


def fetch_all():
    """Return a list of all sites"""
    return [Paper(row) for row in execute_sql("SELECT * FROM paperTable")]


def fetch_by_doi(doi):
    """Fetch the site by id
Params
------
doi: String
    The major zone of the site
"""
    return Paper(execute_sql(
        f"SELECT * FROM paperTable WHERE doi='{doi}'").fetchone())


def fetch_by_sql(clause, param):
    """Fetch sites by query
clause: String
    Contains the clause for the query. SELECT will be added automatically.
    eg: "WHERE title='?'"
params: Tuple = ()
    Arguments to add to clause
"""
    query = '''SELECT * from paperTable ''' + clause
    return [Paper(row) for row in execute_sql(query, param)]


def init_db():
    _create_table()
    pprsite_map.init_db()

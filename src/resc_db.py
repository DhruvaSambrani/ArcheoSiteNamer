
from dbhelper import execute_sql, init_db
init_db()


class Researcher:
    pass


HEADERS = [
    "Researcher",
    "Researcher ID",
    "Laboratory",
    "E-mail ID"]
_ATTRMAP = {
    "researcher": 0,
    "rescID": 1,
    "lab": 2,
    "email": 3}


class Researcher:
    """ The Researcher object is a representation of a database with the
        following attributes:
    Attributes
    ------
    researcher
    researcher ID
    Laboratory
    Email ID

    Functions
    ---------
        __init__(self, row: iterable)
        __str__(self)
        insert(self)
        delete(self)
"""
    researcher: str
    rescID: str
    lab: str
    email: str

    def __init__(self, row):
        """ Constructor
Parameters
------
self: Researcher
row: iterable
    iterable indexed according _ATTRMAP
"""
        self.researcher = row[_ATTRMAP["researcher"]]
        self.rescID = row[_ATTRMAP["rescID"]]
        self.lab = row[_ATTRMAP["lab"]]
        self.email = row[_ATTRMAP["email"]]

    def __str__(self):
        temp = {}
        temp["Researcher"] = self.researcher
        temp["rescID"] = self.rescID
        temp["lab"] = self.lab
        temp["EmailID"] = self.email
        return temp.__str__()

    def insert(self):
        """ Inserts self into database"""
        execute_sql(
            "INSERT INTO rescTable VALUES (?,?,?,?)",
            (self.researcher,
             self.rescID,
             self.lab,
             self.email))

    def delete(self):
        """Deletes self from database."""
        execute_sql(
            f'''
            DELETE FROM "rescTable"
            where rescID='{self.rescID}' ''')


def _create_table():
    execute_sql('''
    CREATE TABLE IF NOT EXISTS "rescTable" (
        "researcher" TEXT NOT NULL,
        "rescID" TEXT NOT NULL
        "lab" TEXT
        "email" TEXT
        PRIMARY KEY("rescID"),
        UNIQUE("rescID")
    )
    ''')


def fetch_all():
    """Return a list of all researchers in the database"""
    return [Researcher(row) for row in execute_sql("SELECT * FROM rescTable")]


def fetch_by_id(rescID):
    """Fetch the researcher by id
Parameters
------
major: rescID
    The unique researcher ID for every researcher
"""
    return Researcher(execute_sql(
        f"SELECT * FROM rescTable WHERE rescID = '{rescID}'").fetchone())


def fetch_by_sql(clause, param):
    """Fetch researcher details by query
clause: String
    Contains the clause for the query. SELECT will be added automatically.
    eg: "WHERE name='?'"
params: Tuple = ()
    Arguments to add to clause
"""
    query = '''SELECT * from rescTable ''' + clause
    return [Researcher(row) for row in execute_sql(query, param)]


_create_table()

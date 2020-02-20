
import sqlite3
from os.path import expanduser as homepath
HEADERS_RESC = [
    "Researcher",
    "Researcher ID",
    "Laboratory ",
    "E-mail ID "]

_ATTRMAP = {
    "researcher": 0,
    "rescID": 1,
    "lab": 2,
    "email": 3}


def _create_table():
    _CURSOR.execute('''
    CREATE TABLE IF NOT EXISTS "researcherTable" (
        "researcher" TEXT NOT NULL,
        "rescID" TEXT NOT NULL,
        "lab" TEXT NOT NULL,
        "email" TEXT NOT NULL
        PRIMARY KEY("rescID"),
        UNIQUE("rescID")
    )
    ''')
    return _CURSOR


def fetch_by_rescID(rescID):
    return [format_row(row) for row in _CURSOR.execute(
        f"SELECT * FROM researcherTable WHERE rescID='{rescID}'")]


def fetch_all_resc():
    return [format_row(row)
            for row in _CURSOR.execute("SELECT * FROM researcherTable")]


def format_row(row):
    temp = []
    temp.append(row[_ATTRMAP["researcher"]])
    temp.append(row[_ATTRMAP["rescID"]])
    temp.append(row[_ATTRMAP["lab"]])
    temp.append(row[_ATTRMAP["email"]])
    return temp


def execute_sql(query):
    _CURSOR.execute(query)


def insert(researcher, rescID, lab, email):
    """
    Inserts values into databas.
    Parameters
    ----------
    researcher
    researcher ID
    Laboratory
    E-mail ID
    """
    _CURSOR.execute(
        "INSERT INTO researcherTable VALUES (?,?,?,?)",
        (researcher,
         rescID,
         lab,
         email))


def delete_all_resc():
    _CURSOR.execute('''DELETE FROM "mainTable"''')


def commit_changes():
    _CONN.commit()


def cleanup():
    _CONN.commit()
    _CONN.close()


# =========== INIT ============== #
_CONN = sqlite3.connect(homepath('~/.ArcheoSiteNamer/database.db'))
_CURSOR = _CONN.cursor()
_create_table()

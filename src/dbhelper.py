import sqlite3
import os.path as path
import os

_DBPATH = None
_CONN = None
_CURSOR = None


def init_db(dbpath='~/.ArcheoSiteNamer/database.db'):
    """Initialise the database connection"""
    global _DBPATH, _CURSOR, _CONN
    if not(_CONN and _CURSOR and _DBPATH):
        _DBPATH = path.expanduser(dbpath)
        print(_DBPATH)
        try:
            _CONN = sqlite3.connect(_DBPATH)
        except sqlite3.OperationalError:
            os.makedirs(path.expanduser('~/.ArcheoSiteNamer'), exist_ok=True)
            _CONN = sqlite3.connect(_DBPATH)

        _CURSOR = _CONN.cursor()


def commit_changes():
    """Commit changes to db"""
    _CONN.commit()


def cleanup():
    """Commit changes and close the db"""
    _CONN.commit()
    _CONN.close()


def execute_sql(query, params=()):
    """Execute a query
query: String
params: Tuple = ()
    Arguments to add to query
"""
    return _CURSOR.execute(query, params)


def delete():
    """Delete the database"""
    cleanup()
    os.remove(_DBPATH)

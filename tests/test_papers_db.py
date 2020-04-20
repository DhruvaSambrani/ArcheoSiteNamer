import sys
sys.path.insert(1, '..')
import test_dbhelper
import papers_db as pdb
from dbhelper import commit_changes as db_commit

s = pdb.Paper(["An intro", "10.5537.848", "A short introduction.",
               "dhruvasambrani19@gmail.com"])
s.insert()
pdb.Paper(["Title", "10.55e7.848", "A short introduction.",
           "dhruvasambrani19@gmail.com"]).insert()


if len(pdb.fetch_all()) != 2:
    raise BaseException("fetch_all failed!")

if pdb.fetch_by_doi("10.5537.848").doi != "10.5537.848":
    raise BaseException("fetch_by_doi failed!")

db_commit()

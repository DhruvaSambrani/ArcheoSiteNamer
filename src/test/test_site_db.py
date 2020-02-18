import sys
sys.path.insert(1, '..')
import test_dbhelper
import site_db as sdb
from dbhelper import commit_changes as db_commit

s = sdb.Site(["A", "B", 12.213, 32.1, "ADC", "name", "desc", ""])
s.insert()
sdb.Site(["A", "B", 12.213, 32.1, "AGC", "name", "desc", ""]).insert()

print("Fetch all")
[print(i) for i in sdb.fetch_all()]

print("\nFetch by id ABAGC")
print(sdb.fetch_by_id("A", "B", "AGC"))

print("\nDeleting all")
# [i.delete() for i in sdb.fetch_all()]

db_commit()

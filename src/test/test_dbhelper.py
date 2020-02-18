import sys
sys.path.insert(1, '..')

import dbhelper

dbhelper.init_db()
print(dbhelper.execute_sql("SELECT * from sqlite_master").fetchone() or "hi")

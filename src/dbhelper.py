import sqlite3
from settings import settings
from os.path import expanduser as homepath

conn = sqlite3.connect(homepath('~/.ArcheoSiteNamer/database.db'))
c = conn.cursor()

headers=["Site Name", "Site Code", "Site Description", "Researcher", "Old Code"]

def createTable():
    c.execute('''
    CREATE TABLE IF NOT EXISTS "mainTable" (
    	"row" TEXT NOT NULL,
    	"column" TEXT NOT NULL,
        "name" TEXT NOT NULL,
    	"abbr" TEXT NOT NULL,
        "description" TEXT,
        "researcher" TEXT NOT NULL,
        "oldcode" TEXT,
    	PRIMARY KEY("row", "column", "abbr"),
        UNIQUE("row", "column", "abbr")
    )
    ''')
    return c
def fetchByID(row, column, abbr):
    return [formatRow(row) for row in c.execute(f"SELECT * FROM mainTable WHERE row = '{row}' AND column = '{column}' AND abbr = '{abbr}'")]

def fetchAll():
    return [formatRow(row) for row in c.execute("SELECT * FROM mainTable ")]

def formatRow(row):
    temp = []
    temp.append(row[2])
    temp.append(row[0]+row[1]+row[3])
    temp.append(row[4][:settings.getint("desc_length")] + (row[4][settings.getint("desc_length"):] and '...'))
    temp.append(row[5])
    temp.append(row[6])
    return temp

def executeSQL(s):
    c.execute(s)

def insert(row, column, name, abbr, description, researcher, oldcode):
    c.execute("INSERT INTO mainTable VALUES (?,?,?,?,?,?,?)", (row, column, name, abbr, description, researcher, oldcode))

def deleteAll():
    c.execute('''DELETE FROM "mainTable"''')
def commitChanges():
    conn.commit()
def cleanup():
    conn.commit()
    conn.close()

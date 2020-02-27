"""
Paper-Site Map
Table Name
----------
pprsiteMap

Attributes
----------
site_id : STRING
ppr_doi : STRING
UNIQUE(site_id, ppr_doi)

Feilds
______
add_entry()
fetch_sites_of_paper()
fetch_by_site()
"""


from dbhelper import execute_sql
import site_db as sdb
import papers_db as pdb


def add_entry(site: sdb.Site, paper: pdb.Paper):
    """Add a site-paper pair."""
    execute_sql(
        '''INSERT into pprsiteMap VALUES(?,?)''', (
            site.get_id(),
            paper.doi
        )
    )


def fetch_sites_of_paper(paper: pdb.Paper):
    """Fetch all sites of a given paper"""
    return [sdb.Site(i) for i in
            execute_sql(
                '''SELECT major_zone, minor_zone,
                        longitude, latitude,
                        abbr, name,
                        siteTable.description, oldcode
                    FROM
                        pprsiteMap
                    INNER JOIN
                        paperTable
                      ON paperTable.doi = pprsiteMap.ppr_doi
                    INNER JOIN
                        siteTable
                      ON pprsiteMap.site_id =
                        siteTable.major_zone||siteTable.minor_zone||siteTable.abbr
                    WHERE doi = ?
                    ''', (paper.doi,)
    )
    ]


def fetch_papers_of_site(site: sdb.Site):
    """Fetch all papers of a given site"""
    return [pdb.Paper(i) for i in
            execute_sql(
                '''SELECT title, doi, paperTable.description, url
                    FROM
                        pprsiteMap
                    INNER JOIN
                        paperTable
                      ON paperTable.doi = pprsiteMap.ppr_doi
                    INNER JOIN
                        siteTable
                      ON pprsiteMap.site_id =
                        siteTable.major_zone||siteTable.minor_zone||siteTable.abbr
                    WHERE major_zone||minor_zone||abbr = ?
                    ''', (site.get_id(),)
    )
    ]


def _create_table():
    execute_sql('''
    CREATE TABLE IF NOT EXISTS "pprsiteMap" (
        "site_id" TEXT NOT NULL,
        "ppr_doi" TEXT NOT NULL,
        PRIMARY KEY("site_id", "ppr_doi"),
        UNIQUE("site_id", "ppr_doi")
    )
    ''')


_create_table()

import sys
sys.path.insert(1, '..')
from dbhelper import delete
try:
    import test_dbhelper
    import test_site_db
    import test_papers_db
    import pprsite_map as psm
    print("add entry...")
    psm.add_entry(test_site_db.s, test_papers_db.s)
    print()
    print("Papers of site: ", test_site_db.s.name)
    [print(i) for i in psm.fetch_papers_of_site(test_site_db.s)]
    print()
    print("Sites of paper: ", test_papers_db.s.doi)
    [print(i) for i in psm.fetch_sites_of_paper(test_papers_db.s)]
    delete()
except Exception as e:
    delete()
    raise(e)

import PySimpleGUIQt as sg
import settings
import site_db as sdb
import papers_db as pdb


sg.theme(settings.SETTINGS["theme"])

sdb.Site(["A", "B", 123, 123, "sda", "name", "desc", ""]).insert()
sdb.Site(["K", "B", 123, 123, "sda", "name", "desc", ""]).insert()
sdb.Site(["J", "B", 123, 123, "sda", "name", "desc", ""]).insert()


def initialise():
    table = sg.Table(
        key="table",
        values=[[""]],
        display_row_numbers=True,
        size_px=(400, 400)
    )
    layout = [
        [sg.Text(
            "ArcheoSiteNamer",
            font="Any 20",
            justification="center",
        )],
        [sg.Combo(
            ['Sites', 'Researchers', 'Papers'],
            key="combo",
            readonly=True,
            enable_events=True
        )],
        [sg.Stretch(), sg.Text('_' * 100), sg.Stretch()],
        [sg.Stretch(), table, sg.Stretch()]
    ]

    window = sg.Window(
        'ArcheoSiteNamer', layout,
        font=('Helvetica', 13),
        size=(500, 500),
        finalize=True
    )
    updateTable(table)

    return window


def updateTable(table: sg.Table, tab: str = "Sites"):
    if tab == "Sites":
        table.update(
            values=[
                [
                    site.majorZone,
                    site.minorZone,
                    str(site.latitude),
                    str(site.longitude),
                    site.abbr,
                    site.name,
                    site.description,
                    site.oldcode
                ]
                for site in sdb.fetch_all()
            ],
            headings=sdb.HEADERS
        )
    elif tab == "Researchers":
        pass
    elif tab == "Papers":
        table.update(
            values=[
                [
                    paper.title,
                    paper.doi,
                    paper.description,
                    paper.url
                ]
                for paper in pdb.fetch_all()
            ],
            headings=pdb.HEADERS
        )


def main():
    window = initialise()
    while True:
        event, values = window.read()
        print(event, values, sep='=>')
        if event is None or event == "Exit":
            break
        if event == "combo":
            updateTable(window.element("table"), values["combo"])

    window.close()


main()

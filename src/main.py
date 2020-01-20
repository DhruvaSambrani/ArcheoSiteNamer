from zonefinder import get_major_zone, get_minor_zone, InvalidLocationError
from settings import SETTINGS, save
import atexit
from tabulate import tabulate
import findaname
from dbhelper import fetch_all, fetch_by_id, HEADERS, delete_all, insert
from dbhelper import initialise as dbinit
from dbhelper import cleanup as dbcleanup
from dbhelper import commit_changes as commitdb


@atexit.register
def cleanup():
    dbcleanup()
    print("Thanks for using!")

# ================= Functions ============== #


def change_settings():
    while True:
        try:
            SETTINGS_INPUT = int(input(
                "Settings Page\n"
                "1. Set length of description to be displayed in Table\n"
                "0. Exit Settings\n"
                "Your option: "
            ))
            if SETTINGS_INPUT == 1:
                while True:
                    inp2 = str(
                        input(f"Old value:{SETTINGS.getint('desc_length')}"
                              "\nNew length = "))
                    if inp2.isnumeric():
                        SETTINGS["desc_length"] = inp2
                        break
                    else:
                        print("Invalid input")
            if SETTINGS_INPUT == 0:
                save()
                break
        except Exception as e:
            print("Program error, notify developers\nSettings:", e)
        print()


def add_site():
    name = str(input("Enter the name of the site: ")).capitalize()
    while True:
        lat = float(input("Latitude of site: "))
        lng = float(input("Longitude of site: "))
        try:
            major_zone = get_major_zone(lat, lng)
            minor_zone = get_minor_zone(lat, lng)
            break
        except InvalidLocationError:
            print("There is no zone here. Check your location again")

    while True:
        abbr = str(input(
            '''Some suggested codes - '''
            f'''{",".join(findaname.findabbrs(name,10))}\n'''
            '''Your preferred 3 character site CODE: ''')).upper()
        if len(abbr) != 3:
            print("Length of CODE must be 3")
        elif len(fetch_by_id(major_zone, minor_zone, abbr)) == 1:
            print("Site CODE already used.")
            print(
                tabulate(
                    fetch_by_id(
                        major_zone,
                        minor_zone,
                        abbr),
                    HEADERS=HEADERS,
                    tablefmt="github"),
                "\n")
        else:
            break

    description = '. '.join(i.capitalize()
                            for i in input("Site description: ").split('. '))
    researcher = str(input("Name of researcher: "))
    oldcode = str(input("Old CODE: "))
    if input(
        f"Site Name - {name}\n"
        f"Site CODE - {major_zone+minor_zone+abbr}\n"
        f"Site Description - {description}\n"
        f"Researcher - {researcher}\n"
        f"Old CODE - {oldcode}\n"
        f"Enter 0 to reject, any key to accept: "
    ) != "0":
        try:
            insert(
                major_zone,
                minor_zone,
                lat,
                lng,
                name,
                abbr,
                description,
                researcher,
                oldcode)
            commitdb()
            print("Site added to database")
        except Exception as e:
            print("Database error - ", e)
    else:
        print("Site add rejected")


class InvalidInputError(Exception):
    """This is not one of the options"""


# ================= Main ============== #
dbinit()
while True:
    try:
        INP = int(input(
            "1. Add a new Site\n"
            "2. List sites by CODE\n"
            "3. List all sites\n"
            "4. Clear all sites\n"
            "5. Settings\n"
            "0. Exit\n"
            "Your input: "))
        if INP == 1:
            add_site()
        elif INP == 2:
            while True:
                CODE = input("Enter CODE: ")
                if len(CODE) == 5:
                    break
                print("Invalid CODE")
            print(tabulate(fetch_by_id(CODE[0],
                                       CODE[1],
                                       CODE[2:]),
                           headers=HEADERS,
                           tablefmt="github"),
                  "\n")
        elif INP == 3:
            print(tabulate(fetch_all(), headers=HEADERS, tablefmt="github"))
        elif INP == 4:
            if input("Are you sure?(y/N)").upper() == "Y":
                delete_all()
                print("Cleared")
        elif INP == 5:
            print()
            change_settings()
        elif INP == 0:
            break
        else:
            raise InvalidInputError("Not a Valid Input")
    except (ValueError, InvalidInputError):
        print("Invalid Input")
    except Exception as e:
        print("Program Error, notify developers - ", e, "")
    print()

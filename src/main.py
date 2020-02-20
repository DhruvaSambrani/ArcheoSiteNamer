from zonefinder import get_major_zone, get_minor_zone, InvalidLocationError
from settings import SETTINGS, save
import atexit
from tabulate import tabulate
import findaname
from site_db import (fetch_all_site, fetch_by_id_site, HEADERS_SITE,
                     delete_all_site, insert_site)
from site_db import cleanup as dbcleanup_site
from site_db import commit_changes as commitdb_site
from resc_db import (fetch_by_rescID, fetch_all_resc, HEADERS_RESC,
                     delete_all_resc, insert_resc)
from site_db import cleanup as dbcleanup_resc
from site_db import commit_changes as commitdb_resc


@atexit.register
def cleanup():
    dbcleanup_site()
    dbcleanup_resc()
    print("Thanks for using!")

# ================= Functions ============== #


def change_settings():
    while True:
        try:
            settings_input = int(input(
                "Settings Page\n"
                "1. Set length of description to be displayed in Table\n"
                "0. Exit Settings\n"
                "Your option: "
            ))
            if settings_input == 1:
                while True:
                    inp2 = str(
                        input(f"Old value:{SETTINGS.getint('desc_length')}"
                              "\nNew length = "))
                    if inp2.isnumeric():
                        SETTINGS["desc_length"] = inp2
                        break
                    else:
                        print("Invalid input")
            if settings_input == 0:
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
        elif len(fetch_by_id_site(major_zone, minor_zone, abbr)) == 1:
            print("Site CODE already used.")
            print(
                tabulate(
                    fetch_by_id_site(
                        major_zone,
                        minor_zone,
                        abbr),
                    HEADERS=HEADERS_SITE,
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
            insert_site(
                major_zone,
                minor_zone,
                lat,
                lng,
                name,
                abbr,
                description,
                researcher,
                oldcode)
            commitdb_site()
            print("Site added to database")
        except Exception as e:
            print("Database error - ", e)
    else:
        print("Site add rejected")


def add_resc():
    researcher = str(input("Name of researcher: "))
    rescID = str(input("Researcher ID: "))
    lab = str(input("Laboratory: "))
    email = str(input("E-mail ID: "))
    if input(
        f"Researcher - {researcher}\n"
        f"ResearcherID - {rescID}\n"
        f"Laboratory - {lab}\n"
        f"EmailID - {email}\n"
        f"Enter 0 to reject, any key to accept: "
    ) != "0":
        try:
            insert_resc(
                researcher,
                rescID,
                lab,
                email)
            commitdb_resc()
            print("Researcher added to database")
        except Exception as e:
            print("Database error - ", e)

    else:
        print("Researcher add rejected")


class InvalidInputError(Exception):
    """This is not one of the options"""


# ================= Main ============== #
while True:
    try:
        INP = int(input(
            "1. Add a new Site\n"
            "2. Add a new Researcher\n"
            "3. List sites by CODE\n"
            "4. List sites by Researcher ID\n"
            "5. List all sites\n"
            "6. List all researchers\n"
            "7. Clear database\n"
            "8. Settings\n"
            "0. Exit\n"
            "Your input: "))
        if INP == 1:
            add_site()
        elif INP == 2:
            add_resc()
        elif INP == 3:
            while True:
                CODE = input("Enter CODE: ")
                if len(CODE) == 5:
                    break
                print("Invalid CODE")
            print(tabulate(fetch_by_id_site(CODE[0],
                                            CODE[1],
                                            CODE[2:]),
                           headers=HEADERS_SITE,
                           tablefmt="github"),
                  "\n")
        elif INP == 4:
            while True:
                ID = input("Enter ID: ")
            print(tabulate(fetch_by_rescID(ID),
                           headers=HEADERS_RESC,
                           tablefmt="github"),
                  "\n")
        elif INP == 5:
            print(tabulate(fetch_all_site(), headers=HEADERS_SITE,
                           tablefmt="github"))
        elif INP == 6:
            print(tabulate(fetch_all_resc(), headers=HEADERS_RESC,
                           tablefmt="github"))
        elif INP == 7:
            print("1. Clear all sites\n",
                  "2. Clear all researchers\n")
            if int(input("Your choice: ")) == 1:
                delete_all_site()
                print("Site database cleared")
            elif int(input("Your choice: ")) == 2:
                delete_all_resc()
                print("Researcher database cleared")
        elif INP == 8:
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

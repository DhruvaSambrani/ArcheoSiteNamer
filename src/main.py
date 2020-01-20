from zonefinder import get_major_zone, get_minor_zone, InvalidLocationError
from settings import SETTINGS, save
import atexit
from tabulate import tabulate
import findaname
from dbhelper import fetch_all, fetch_by_id, headers, createTable, insert
from dbhelper import delete_all, cleanup as dbcleanup, commit_changes as commit


@atexit.register
def cleanup():
    dbcleanup()
    print("Thanks for using!")

# ================= Functions ============== #


def change_settings():
    while True:
        try:
            inp = int(input(
                "Settings Page\n"
                "1. Set length of description to be displayed in Table\n"
                "0. Exit Settings\n"
                "Your option: "
            ))
            if inp == 1:
                while True:
                    inp2 = str(
                        input(f"Old value:{SETTINGS.getint('desc_length')}"
                              "\nNew length = "))
                    if inp2.isnumeric():
                        SETTINGS["desc_length"] = inp2
                        break
                    else:
                        print("Invalid input")
            if inp == 0:
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
            majorZone = get_major_zone(lat, lng)
            minorZone = get_minor_zone(lat, lng)
            break
        except InvalidLocationError:
            print("There is no zone here. Check your location again")

    while True:
        abbr = str(input(
            '''Some suggested codes - '''
            f'''{",".join(findaname.findabbrs(name,10))}\n'''
            '''Your preferred 3 character site code: ''')).upper()
        if len(abbr) != 3:
            print("Length of code must be 3")
        elif len(fetch_by_id(majorZone, minorZone, abbr)) == 1:
            print("Site Code already used.")
            print(
                tabulate(
                    fetch_by_id(
                        majorZone,
                        minorZone,
                        abbr),
                    headers=headers,
                    tablefmt="github"),
                "\n")
        else:
            break

    description = '. '.join(i.capitalize()
                            for i in input("Site description: ").split('. '))
    researcher = str(input("Name of researcher: "))
    oldcode = str(input("Old code: "))
    if input(
        f"Site Name - {name}\n"
        f"Site Code - {majorZone+minorZone+abbr}\n"
        f"Site Description - {description}\n"
        f"Researcher - {researcher}\n"
        f"Old Code - {oldcode}\n"
        f"Enter 0 to reject, any key to accept: "
    ) != "0":
        try:
            insert(
                majorZone,
                minorZone,
                lat,
                lng,
                name,
                abbr,
                description,
                researcher,
                oldcode)
            commit()
            print("Site added to database")
        except Exception as e:
            print("Database error - ", e)
    else:
        print("Site add rejected")


# ================= Main ============== #
createTable()
st = True


class InvalidInputError(Exception):
    """This is not one of the options"""


while True:
    try:
        inp = int(input(
            "1. Add a new Site\n"
            "2. List sites by code\n"
            "3. List all sites\n"
            "4. Clear all sites\n"
            "5. Settings\n"
            "0. Exit\n"
            "Your input: "))
        if inp == 1:
            add_site()
        elif inp == 2:
            while True:
                code = input("Enter Code: ")
                if len(code) == 5:
                    break
                print("Invalid Code")
            print(tabulate(fetch_by_id(code[0],
                                       code[1],
                                       code[2:]),
                           headers=headers,
                           tablefmt="github"),
                  "\n")
        elif inp == 3:
            print(tabulate(fetch_all(), headers=headers, tablefmt="github"))
        elif inp == 4:
            if input("Are you sure?(y/N)").upper() == "Y":
                delete_all()
                print("Cleared")
        elif inp == 5:
            print()
            change_settings()
        elif inp == 0:
            break
        else:
            raise InvalidInputError("Not a Valid Input")
    except (ValueError, InvalidInputError):
        print("Invalid Input")
    except Exception as e:
        print("Program Error, notify developers - ", e, "")
    print()

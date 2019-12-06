import findaname
from dbhelper import fetchAll, fetchByID, headers, cleanup as dbcleanup, createTable, insert, deleteAll, commitChanges as commit
from tabulate import tabulate
import atexit
from settings import changeSettings as Settings

@atexit.register
def cleanup():
    dbcleanup()
    print("Thanks for using!")

# ================= Functions ============== #
def addSite():
    name = str(input("Enter the name of the site: ")).capitalize()
    while True:
        row = str(input("Row Value of site: ")).upper()
        column = str(input("Column Value of site: ")).upper()
        if len(row)!=1 or len(column)!=1:
            print("Length of Row and column must be 1")
        else:
            break
    while True:
        abbr = str(input(f'''Some suggested codes - {", ".join(findaname.findabbrs(name,10))}\nYour preferred 3 character site code: ''')).upper()
        if len(abbr) != 3:
            print("Length of code must be 3")
        elif len(fetchByID(row,column,abbr)) == 1:
            print("Site Code already used.")
            print(tabulate(fetchByID(row,column,abbr), headers=headers, tablefmt="github"), "\n")
        else:
            break

    description = '. '.join(i.capitalize() for i in input("Site description: ").split('. '))
    researcher = str(input("Name of researcher: "))
    oldcode = str(input("Old code: "))
    if input(
        f"Site Name - {name}\n"
        f"Site Code - {row+column+abbr}\n"
        f"Site Description - {description}\n"
        f"Researcher - {researcher}\n"
        f"Old Code - {oldcode}\n"
        f"Enter 0 to reject, any key to accept: "
    ) != "0":
        try :
            insert(row, column, name, abbr, description, researcher, oldcode)
            commit()
            print("Site added to database")
        except Exception as e:
            print("Database error - ",e)
    else:
        print("Site add rejected")

# ================= Main ============== #
createTable()
st = True
class InvalidInputError(Exception):
    """This is not one of the options"""
    pass

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
            addSite()
        elif inp == 2:
            while True:
                code = input("Enter Code: ")
                if len(code)==5:
                    break
                print("Invalid Code")
            print(tabulate(fetchByID(code[0],code[1],code[2:]), headers=headers, tablefmt="github"), "\n")
        elif inp == 3:
            print(tabulate(fetchAll(),headers=headers, tablefmt="github"))
        elif inp == 4:
            if(input("Are you sure?(y/N)").upper()=="Y"):
                deleteAll()
                print("Cleared")
        elif inp == 5:
            print()
            Settings()
        elif inp == 0:
            break
        else:
            raise InvalidInputError("Not a Valid Input")
    except (ValueError, InvalidInputError):
        print("Invalid Input")
    except Exception as e:
        print("Program Error, notify developers - ", e,"")
    print()

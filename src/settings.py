import configparser
from os.path import expanduser as homepath, exists as fileExists
from os import makedirs

settingsFilePath = homepath('~/.ArcheoSiteNamer/settings.ini')

def resetToDefaults():
    config["SETTINGS"]={}
    settings = config["SETTINGS"]
    settings["desc_length"] = "20"
    save()
def changeSettings():
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
                    inp2 = str(input(f"Old value:{settings.getint('desc_length')}\nNew length = "))
                    if inp2.isnumeric():
                        settings["desc_length"] = inp2
                        break
                    else :
                        print("Invalid input")
            if inp == 0:
                save()
                break
        except Exception as e:
            print("Program error, notify developers\nSettings:", e)
        print()
def save():
    with open(settingsFilePath, 'w') as configfile:
        config.write(configfile)
def initialise():
    makedirs(homepath('~/.ArcheoSiteNamer'),exist_ok=True)
    if (fileExists(settingsFilePath)):
        try:
            config.read(settingsFilePath)
            global settings
            settings = config["SETTINGS"]
            if not settings.getint("desc_length"):
                raise Exception("Corrupt Settings Values")
        except Exception as e:
            print(e)
            print("Settings file is corrupt. Edit the file directly or reset to default.")
            print(settingsFilePath)
            with open(settingsFilePath,"r") as f:
                print(f.read())
            if input("Reset ALL Settings to default? Y to reset, any key to exit: ").upper()=="Y":
                resetToDefaults()
                initialise()
            else:
                print("Exiting...")
                exit()
    else:
        resetToDefaults()
        initialise()

config = configparser.ConfigParser()
settings = {}
initialise()

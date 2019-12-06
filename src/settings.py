import configparser
import os.path

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
    with open('inits.ini', 'w') as configfile:
        config.write(configfile)
def initialise():
    if (os.path.exists("inits.ini")):
        try:
            config.read('inits.ini')
            global settings
            settings = config["SETTINGS"]
            if not settings.getint("desc_length"):
                raise Exception("Corrupt Settings Values")
        except Exception as e:
            print(e)
            print("Settings file is corrupt. Edit the file directly or reset to default.")
            print("inits.ini")
            with open("inits.ini","r") as f:
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
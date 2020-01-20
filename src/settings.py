import configparser
from os.path import expanduser as homepath, exists as fileExists
from os import makedirs

_settings_file_path = homepath('~/.ArcheoSiteNamer/settings.ini')


def reset_to_defaults():
    _config["SETTINGS"] = {}
    global SETTINGS
    SETTINGS = _config["SETTINGS"]
    SETTINGS["desc_length"] = "20"
    save()


def save():
    with open(_settings_file_path, 'w') as _configfile:
        _config.write(_configfile)


def initialise():
    makedirs(homepath('~/.ArcheoSiteNamer'), exist_ok=True)
    if fileExists(_settings_file_path):
        try:
            _config.read(_settings_file_path)
            global SETTINGS
            SETTINGS = _config["SETTINGS"]
            if not SETTINGS.getint("desc_length"):
                raise Exception("Corrupt Settings Values")
        except Exception as e:
            print(e)
            print("Settings file is corrupt."
                  " Edit the file directly or reset to default.")
            print(_settings_file_path)
            with open(_settings_file_path, "r") as file:
                print(file.read())
            if input(
                    "Reset ALL Settings to default? "
                    "Y to reset, any key to exit: ").upper() == "Y":
                reset_to_defaults()
                initialise()
            else:
                print("Exiting...")
                exit()
    else:
        reset_to_defaults()
        initialise()


_config = configparser.configParser()
SETTINGS = {}
initialise()

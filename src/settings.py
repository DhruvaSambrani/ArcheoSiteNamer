import configparser
from os.path import expanduser as homepath, exists as fileExists
from os import makedirs

_SETTINGS_FILE_PATH = homepath('~/.ArcheoSiteNamer/settings.ini')


def reset_to_defaults(settings_dict):
    _CONFIG["SETTINGS"] = {}
    settings_dict = _CONFIG["SETTINGS"]
    settings_dict["desc_length"] = "20"
    save()


def save():
    with open(_SETTINGS_FILE_PATH, 'w') as _configfile:
        _CONFIG.write(_configfile)


class CorruptSettingsError(Exception):
    """Settings file is corrupt"""


def initialise(settings_dict):
    makedirs(homepath('~/.ArcheoSiteNamer'), exist_ok=True)
    if fileExists(_SETTINGS_FILE_PATH):
        try:
            _CONFIG.read(_SETTINGS_FILE_PATH)
            settings_dict = _CONFIG["SETTINGS"]
            if not settings_dict.getint("desc_length"):
                raise CorruptSettingsError("Corrupt Settings Values")
        except CorruptSettingsError as e:
            print(e)
            print("Settings file is corrupt."
                  " Edit the file directly or reset to default.")
            print(_SETTINGS_FILE_PATH)
            with open(_SETTINGS_FILE_PATH, "r") as file:
                print(file.read())
            if input(
                    "Reset ALL Settings to default? "
                    "Y to reset, any key to exit: ").upper() == "Y":
                reset_to_defaults()
                initialise(settings_dict)
            else:
                print("Exiting...")
                exit()
    else:
        reset_to_defaults()
        initialise()


_CONFIG = configparser.configParser()
SETTINGS = {}
initialise(SETTINGS)

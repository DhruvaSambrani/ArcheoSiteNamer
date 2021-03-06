import configparser
from os.path import expanduser as homepath, exists as fileExists
from os import makedirs

_SETTINGS_FILE_PATH = homepath('~/.ArcheoSiteNamer/settings.ini')


def reset_to_defaults():
    """Reset settings to defaults"""
    _CONFIG["SETTINGS"] = {}
    _CONFIG["SETTINGS"]["desc_length"] = "20"
    _CONFIG["SETTINGS"]["theme"] = "Dark Brown"
    save()
    return _CONFIG["SETTINGS"]


def save():
    """Save changes to settings file"""
    with open(_SETTINGS_FILE_PATH, 'w') as _configfile:
        _CONFIG.write(_configfile)


class CorruptSettingsError(Exception):
    """Settings file is corrupt"""


def initialise():
    """init the SETTINGS object"""
    makedirs(homepath('~/.ArcheoSiteNamer'), exist_ok=True)
    if fileExists(_SETTINGS_FILE_PATH):
        try:
            _CONFIG.read(_SETTINGS_FILE_PATH)
            try:
                _CONFIG["SETTINGS"].getint("desc_length")
                return _CONFIG["SETTINGS"]
            except Exception:
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
                return initialise()
            print("Exiting...")
            exit()
    else:
        reset_to_defaults()
        return initialise()


_CONFIG = configparser.ConfigParser()
SETTINGS = initialise()

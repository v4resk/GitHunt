import configparser
import os
from pathlib import Path

def get_project_root() -> Path:
    return Path(__file__).parent.parent


class Config(object):
    def __init__(self, auto_load: bool = True):
        self.config = configparser.ConfigParser(allow_no_value=True, interpolation=configparser.ExtendedInterpolation())
        self.default_config = os.path.join(get_project_root(), "config", "default.ini")
        self.file = os.path.join(get_project_root(), "config", "config.ini")
        if not os.path.isfile(self.file):
            self.write_default()
        if auto_load:
            self.load_config()

    def load_config(self, filename=None):
        if filename:
            self.file = Path(filename).absolute()
        try:
            self.config.read(self.file)
        except FileNotFoundError:
            print("The file specified does not exists")
            self.write_default()
        except configparser.ParsingError:
            print("Error encountered while parsing, check configuration file syntax")
        except Exception as e:
            print("Unhandled exception, contact support")
            print(f"Exception : {e}")

    def save_config(self):
        with open(self.file, 'w') as configfile:
            self.config.write(configfile)

    def get_config(self):
        return self.config

    def get_section(self, s):
        return self.config[s]


    def get(self, s, v):
        try:
            return self.config[s][v]
        except KeyError:
            return None

    def set(self, s, v, new_value):
        self.config[s][v] = new_value

    def write_default(self):
        content = open(self.default_config).read()
        with open(self.file, "w") as default:
            default.write(content)


if __name__ == "__main__":
    c = Config()
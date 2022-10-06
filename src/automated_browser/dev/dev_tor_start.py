# Package Library
from FirefoxDriver.driver.firefox import Firefox


if __name__ == "__main__":
    driver = Firefox(onion_network=True)

    driver.get("https://google.com")


import json
import FirefoxDriver


json_path = "D:/Github/FirefoxDriver/src/FirefoxDriver/data/settings/browser_settings.json"

from importlib_resources import files


settings_path = (
    files(FirefoxDriver)
    .joinpath("data")
    .joinpath("settings")
    .joinpath("browser_settings.json")
)


from pathlib import Path
t1 = Path(settings_path)


type(settings_path)




with open(settings_path, "r") as read_file:
    settings_dict = json.load(read_file)


import regex as re

re_ld = re.compile("__")
re_sd = re.compile("_")


output_dict: dict[str, int | str | bool] = {
    re_sd.sub(".", re_ld.sub("-", k)): v for k, v in settings_dict.items()
}


def get_settings():
    output_dict: dict[str, int | str | bool] = {
        re.sub("__", "-", k): v for k, v in settings_dict.items()
    }
    output_dict_fin: dict[str, int | str | bool] = {
        re.sub("_", ".", k): v for k, v in output_dict.items()
    }

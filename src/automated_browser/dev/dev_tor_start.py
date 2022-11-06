# Standard Library
import json
from pathlib import Path

# Thirdparty Library
import FirefoxDriver
import regex as re
from importlib_resources import files

# Package Library
from automated_browser.driver.filepaths import FilePaths
from automated_browser.driver.firefox import Firefox
from automated_browser.driver.torbrowser import TorBrowser


driver = TorBrowser()


dir(driver)


tor_exe = driver.start_tor(t_max=80)





file_paths = FilePaths()


dir(file_paths)


file_paths.tor_path




if __name__ == "__main__":
    driver = Firefox(onion_network=True)

    driver.get("https://google.com")




json_path = "D:/Github/FirefoxDriver/src/FirefoxDriver/data/settings/browser_settings.json"



settings_path = (
    files(FirefoxDriver)
    .joinpath("data")
    .joinpath("settings")
    .joinpath("browser_settings.json")
)


t1 = Path(settings_path)


type(settings_path)




with open(settings_path, "r") as read_file:
    settings_dict = json.load(read_file)



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

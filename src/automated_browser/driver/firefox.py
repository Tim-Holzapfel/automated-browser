"""Driver on which all of the package builds."""

# Standard Library
import json
from os import devnull
from pathlib import Path
from time import sleep

# Thirdparty Library
import regex as re
from func_timeout import func_set_timeout
from importlib_resources import files
from regex import Pattern
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# Package Library
from automated_browser.driver.filepaths import FilePaths
from automated_browser.driver.torbrowser import TorBrowser, java_kill


class Firefox(WebDriver, FilePaths):
    """Start Firefox Browser.

    Generate a Firefox Browser while routing traffic through Tor.


    Attributes
    ----------
    headless: bool
        Start browser without an user interface.
    onion_network: bool
        Route the incoming and outgoing traffic through the onion network.
    settings_path: Path
        Path to the browser settings json file.

    Methods
    -------
    close_browser():
        Close browser and kill all processes.
    find_by_css():
    find_all_by_css(css_selector):
        Prints the person's name and age.
    wait_for_element_presence():
    wait_for_element_clickable():
    find_button(css_selector, selector_type):
        Find button using selector and click it.
    """

    def __init__(
        self,
        headless: bool = False,
        onion_network: bool = True,
        accept_insecure_certs: bool = True,
    ) -> None:
        """
        Start a Firefox and optionally route traffic through Tor.

        Parameters
        ----------
        headless : bool, optional
            Start the browser with a GUI, by default False.
        onion_network : bool, optional
            Route the traffic through the onion network, by default True.
        accept_insecure_certs : bool, optional
            Accept insecure certicates, by default True.
        """
        self.headless: bool = headless
        self.accept_insecure_certs: bool = accept_insecure_certs
        self.onion_network: bool = onion_network
        self.re_ld: Pattern[str] = re.compile("__")
        self.re_sd: Pattern[str] = re.compile("_")
        self.settings_path: Path = Path(
            str(
                files("automated_browser")
                .joinpath("data")
                .joinpath("settings")
                .joinpath("browser_settings.json")
            )
        )
        profile: FirefoxProfile = FirefoxProfile()
        options: Options = Options()
        options.headless = self.headless
        options.accept_insecure_certs = self.accept_insecure_certs

        if self.onion_network:
            tor_inst: TorBrowser = TorBrowser()
            self.tor_exe = tor_inst.start_tor(t_max=80)
            browser_prefs: dict[str, int | str | bool] = self.get_settings()
            options.preferences.update(browser_prefs)
            profile.default_preferences.update(browser_prefs)

        super().__init__(
            firefox_profile=profile,
            options=options,
            executable_path=self.geckodriver_path.as_posix(),
            service_log_path=devnull,
        )

        self.maximize_window()

        self.delete_all_cookies()

    @func_set_timeout(timeout=80)
    def close_browser(self) -> None:
        """Close the Browser."""
        # Close driver window
        self.close()
        sleep(1)
        java_kill()
        if self.onion_network:
            # Terminate the tor exe
            self.tor_exe.terminate()
            sleep(1)
            # Kill all process related to the driver to make sure it is closed
            java_kill()

    @func_set_timeout(timeout=80)
    def refresh_page(self) -> None:
        """Refresh webpage."""
        self.refresh()

    @func_set_timeout(timeout=80)
    def find_by_css(self, css_value: str) -> WebElement:
        """Find webelement by css selector.

        Parameters
        ----------
        css_value : str
            CSS locator string.

        Returns
        -------
        WebElement
        """
        return self.find_element(by=By.CSS_SELECTOR, value=css_value)

    @func_set_timeout(timeout=80)
    def find_all_by_css(self, css_value: str) -> list[WebElement]:
        """Find all webelement by css selector.

        Parameters
        ----------
        css_value : str
            CSS locator string.

        Returns
        -------
        list[WebElement]
        """
        return self.find_elements(by=By.CSS_SELECTOR, value=css_value)

    @func_set_timeout(timeout=80)
    def wait_for_element_presence(
        self, css_value: str, timeout_secs: int = 90
    ) -> WebElement:
        """Wait for the presence of the element to be located.

        Parameters
        ----------
        css_value : str
            CSS locator string.
        timeout_secs : int, optional
            Seconds until a timeout exception is raised. The default is 90.

        Raises
        ------
        TimeoutException
            If the element could not be located within the given timeframe.

        Returns
        -------
        WebElement
        """
        return WebDriverWait(self, timeout_secs).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, css_value))
        )

    @func_set_timeout(timeout=80)
    def wait_for_element_clickable(
        self, css_value: str, timeout_secs: int = 90
    ) -> WebElement:
        """Wait for the element to be clickable.

        Parameters
        ----------
        css_value : str
            CSS locator string.
        timeout_secs : int, optional
            Seconds until a timeout exception is raised. The default is 90.

        Raises
        ------
        TimeoutException
            If the element could not be located within the given timeframe.

        Returns
        -------
        WebElement
        """
        return WebDriverWait(self, timeout_secs).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, css_value))
        )

    @func_set_timeout(timeout=80)
    def find_button(
        self, css_selector: str, timeout_secs: int = 90
    ) -> WebElement:
        """Find button using CSS selector and click it.

        Parameters
        ----------
        css_value : str
            CSS locator string.
        timeout_secs : int, optional
            Seconds until a timeout exception is raised. The default is 90.

        Raises
        ------
        TimeoutException
            If the element could not be located within the given timeframe.

        Returns
        -------
        WebElement
        """
        button_field = self.wait_for_element_clickable(
            css_selector, timeout_secs
        )

        button_field.click()

        return button_field

    def get_settings(self) -> dict[str, int | str | bool]:
        """Replace dictionary keys.

        Returns
        -------
        output_dict : dict
            Dictionary constructed from input.
        """
        with open(str(self.settings_path), mode="r") as read_file:
            settings_dict = json.load(read_file)

        # Replace dict keys
        output_dict: dict[str, int | str | bool] = {
            self.re_sd.sub(".", self.re_ld.sub("-", k)): v
            for k, v in settings_dict.items()
        }

        return output_dict

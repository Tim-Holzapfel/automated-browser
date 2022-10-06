"""File paths used within the project."""

# Standard Library
from os import getenv
from pathlib import Path

# Thirdparty Library
from importlib_resources import files
from webdrivermanager import GeckoDriverManager

# Package Library
import FirefoxDriver


class FilePaths:
    """
    Project specific paths to files.

    Attributes
    ----------
    desktop_path_user : Path
        Path to the User Desktop.
    tor_path : Path
        Path to the Tor executable.
    user_home_dir : str
        Path to the user home directory.
    exe_dir_user : str
        Path to the user executable.
    geckodriver_path : Path
        Path to the geckodriver executable.

    """

    def __init__(self) -> None:
        # Base Directories
        self._internal_dir: Path = Path(
            str(files(FirefoxDriver).joinpath("data"))
        )
        self.desktop_path_user: Path = Path(self.user_home_dir) / "Desktop"
        self.tor_path: Path = (
            self.desktop_path_user / "Tor Browser" / "Browser" / "firefox.exe"
        )

    @property
    def user_home_dir(self) -> str:
        user_home_dir: str | None = getenv("USERPROFILE")
        if not user_home_dir:
            raise ValueError(
                "The environment variable 'USERPROFILE' has not been set yet!"
            )
        return user_home_dir

    @property
    def exe_dir_user(self) -> Path:
        exe_dir_user: Path = self._internal_dir / "executables"
        exe_dir_user.mkdir(exist_ok=True)
        return exe_dir_user

    @property
    def geckodriver_path(self) -> Path:
        geckodriver_path: Path = self.exe_dir_user / "geckodriver.exe"

        if not geckodriver_path.exists():
            gdd: GeckoDriverManager = GeckoDriverManager(
                download_root=self.exe_dir_user,
                link_path=self.exe_dir_user,
                os_name="win",
            )
            gdd.download_and_install()

        return geckodriver_path

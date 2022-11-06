"""File paths used within the project."""

# Standard Library
from os import getenv
from pathlib import Path

# Thirdparty Library
from importlib_resources import files
from webdrivermanager import GeckoDriverManager


class FilePaths:
    """
    Project specific paths.

    Attributes
    ----------
    user_home_dir : str
        Path to the user home directory.
    desktop_path_user : Path
        Path to the User Desktop.
    tor_path : Path
        Path to the Tor executable.
    geckodriver_path : Path
        Path to the geckodriver executable.

    """

    def __init__(self) -> None:
        """
        Project specific paths.

        Returns
        -------
        None.
        """
        self._internal_dir: Path = Path(
            str(files("automated_browser").joinpath("data"))
        )

    @property
    def user_home_dir(self) -> str:
        """
        Get the path to the home directory of the user.

        Returns
        -------
        str
            Home directory of the user.

        Raises
        ------
        ValueError
            If the environment variable 'USERPROFILE' has not been set.
        """
        user_home_dir: str | None = getenv("USERPROFILE")
        if not user_home_dir:
            raise ValueError(
                "The environment variable 'USERPROFILE' has not been set yet!"
            )
        return user_home_dir

    @property
    def desktop_path_user(self) -> Path:
        """
        Get the path to the home directory of the user.

        Returns
        -------
        Path
            Home directory of the user.
        """
        return Path(self.user_home_dir) / "Desktop"

    @property
    def tor_path(self) -> Path:
        """
        Get the path to the Tor executable.

        Returns
        -------
        Path
            Path to the Tor executable.
        """
        return (
            self.desktop_path_user / "Tor Browser" / "Browser" / "firefox.exe"
        )

    @property
    def geckodriver_path(self) -> Path:
        """
        Get the path to the geckodriver executable.

        Returns
        -------
        Path
            Path to the geckodriver executable.
        """
        # Path to the internal user directory.
        exe_dir_user: Path = self._internal_dir / "executables"
        # Create folder if it does not already exist.
        exe_dir_user.mkdir(exist_ok=True)

        # Path to the geckodriver executable.
        geckodriver_path: Path = exe_dir_user / "geckodriver.exe"

        if not geckodriver_path.exists():
            gdd: GeckoDriverManager = GeckoDriverManager(
                download_root=exe_dir_user,
                link_path=exe_dir_user,
                os_name="win",
            )
            gdd.download_and_install()

        return geckodriver_path

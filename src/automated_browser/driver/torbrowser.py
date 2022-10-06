"""Utility functions."""

# Standard Library
import atexit

from functools import partialmethod
from subprocess import Popen
from time import perf_counter
from typing import Any, Literal, Optional

# Thirdparty Library
import regex as re
import win32con
import win32gui

from func_timeout import func_set_timeout
from psutil import NoSuchProcess, process_iter, wait_procs
from regex import Pattern
from termcolor import colored

# Package Library
from FirefoxDriver.driver.filepaths import FilePaths


@atexit.register
def java_kill() -> None:
    """Terminate all processes associated with the scraping."""
    p_pat: Pattern[str] = re.compile(
        r"(jqs|javaw|java|geckodriver|phantomjs|firefox)\.exe"
    )
    for process in (procs := process_iter(["name"])):
        proc_name: str | None = process.info.get("name")
        assert isinstance(proc_name, str)
        if bool(p_pat.match(proc_name)):
            try:
                process.terminate()
            except NoSuchProcess:
                pass
    _, alive = wait_procs(procs, timeout=10)
    for process in alive:
        p_name: str | None = process.info.get("name")
        assert isinstance(p_name, str)
        if bool(p_pat.match(p_name)):
            try:
                process.terminate()
            except NoSuchProcess:
                pass


class TorBrowser(FilePaths):
    def __init__(self) -> None:
        self.tor_pat: Pattern[str] = re.compile(r"^About\sTor.*Tor\sBrowser$")
        self.proc_list: list[str] = []

    def enum_callback(
        self,
        hwnd: str,
        extra: Optional[Any] = None,  # pylint: disable=unused-argument
    ) -> None:
        """Enumerate callback function."""
        if bool(self.tor_pat.search(win32gui.GetWindowText(hwnd))):
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
            self.proc_list.append(hwnd)

    @func_set_timeout(timeout=80)
    def start_tor(self, t_max: int = 80) -> Popen[bytes]:
        """
        _summary_

        Parameters
        ----------
        t_max : int, optional
            _description_, by default 80

        Returns
        -------
        Popen[bytes]
            _description_
        """
        self.print_method_init("start_tor", "I will try to start TOR now...")
        java_kill()
        tor_exe: Popen[bytes] = Popen(self.tor_path)

        t_start: float = perf_counter()
        while True:
            win32gui.EnumWindows(self.enum_callback, None)
            diff_t: float = round(t_max - (perf_counter() - t_start), 1)
            self.print_counter(
                "start_tor",
                f"I'm waiting for TOR to start...({diff_t}s until timeout)",
            )
            if any(self.proc_list):
                print("")
                self.print_method_success(
                    "start_tor", "I successfully started TOR!"
                )
                break

        return tor_exe

    def _print(
        self,
        method: str,
        msg: str,
        print_col: Literal[
            "red", "green", "yellow", "blue", "magenta", "cyan", "white"
        ],
    ) -> None:
        """
        _summary_

        Parameters
        ----------
        method : str
            _description_
        msg : str
            _description_
        print_col : Literal["red", "green", "yellow", "blue", "magenta",
        "cyan", "white"]
            _description_
        """
        msg_join: str = " ".join(msg.split())
        method_col: str = colored(
            text=method, color=print_col, attrs=["bold"]
        )
        print(method_col, msg_join, sep=": ", flush=True)

    print_method_init: partialmethod[None] = partialmethod(
        _print, print_col="blue"
    )

    print_method_success: partialmethod[None] = partialmethod(
        _print, print_col="green"
    )

    def print_counter(self, method: str, msg: str) -> None:
        """Return print statement with the desired color."""
        msg_join: str = " ".join(msg.split())
        method_col: str = colored(text=method, color="red", attrs=["bold"])
        print(
            "\r" + method_col + ": " + msg_join + "\r",
            end="",
            sep="",
            flush=True,
        )

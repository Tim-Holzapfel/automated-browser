# automated-browser

A completely automated Firefox browser.

# Usage
The main workhorse of this project is the `Firefox` class that will start a Firefox marionette.
```
from automated_browser.driver.firefox import Firefox
driver = Firefox(
        headless=False, onion_network=True, accept_insecure_certs=True
    )
driver.go("https://github.com)
```

# Requirements
- A working installation of either the [Firefox Browser](https://www.mozilla.org/en-US/firefox/new/) or the [Firefox Browser Developer Edition](https://www.mozilla.org/en-US/firefox/developer/) is required for this package to work.
- (Optional) A working installation of [Tor](https://www.torproject.org/). If Tor cannot be found then it will be downloaded by the package if access to the Onion Network is desired.

# Notes
It might be necessary to start Tor and to connect to the internet by using Tor before using the package.

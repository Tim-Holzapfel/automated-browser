"""Main package script."""

# Package Library
from automated_browser.driver.firefox import Firefox


if __name__ == "__main__":
    driver: Firefox = Firefox(
        headless=False, onion_network=True, accept_insecure_certs=True
    )

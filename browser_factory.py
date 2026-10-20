import os
from pathlib import Path
from shutil import which

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService


class BrowserFactory:
    SUPPORTED = ("chrome", "firefox")

    @classmethod
    def create(cls, browser, headless=True):
        if browser not in cls.SUPPORTED:
            raise ValueError(f"Неизвестный браузер '{browser}'. Доступны: chrome, firefox.")
        if browser == "chrome":
            options = webdriver.ChromeOptions()
            options.set_capability("goog:loggingPrefs", {"browser": "ALL", "performance": "ALL"})
            if headless:
                options.add_argument("--headless=new")
            options.add_argument("--disable-dev-shm-usage")
            if os.getenv("CHROME_BINARY"):
                options.binary_location = os.environ["CHROME_BINARY"]
            path = os.getenv("CHROMEDRIVER") or which("chromedriver")
            driver = webdriver.Chrome(service=ChromeService(executable_path=path), options=options)
        else:
            options = webdriver.FirefoxOptions()
            if headless:
                options.add_argument("-headless")
            if os.getenv("FIREFOX_BINARY"):
                options.binary_location = os.environ["FIREFOX_BINARY"]
            path = os.getenv("GECKODRIVER") or which("geckodriver")
            snap_directory = Path("/snap/firefox/current/usr/lib/firefox")
            if (
                not os.getenv("GECKODRIVER") and path
                and Path(path).parent == Path("/snap/bin")
                and (snap_directory / "geckodriver").is_file()
                and (snap_directory / "firefox").is_file()
            ):
                # Snap-обёртка запрещает Selenium завершать сервис сигналом.
                path = str(snap_directory / "geckodriver")
                if not os.getenv("FIREFOX_BINARY"):
                    options.binary_location = str(snap_directory / "firefox")
            driver = webdriver.Firefox(service=FirefoxService(executable_path=path), options=options)
        try:
            driver.set_window_size(1600, 1000)
            driver.set_page_load_timeout(45)
        except Exception:
            try:
                driver.quit()
            except Exception:
                pass
            raise
        return driver

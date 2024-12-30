from trip import Trip

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from pyppeteer import launch


class BaseTripPageParser:
    class AvailabilityException(Exception):
        """Exception raised when availxability status cannot be determined."""

        def __init__(self, message="Could not determine availability status"):
            super().__init__(message)

    def parse(self):
        raise NotImplementedError

    def _check_availability(self):
        raise NotImplementedError

    def _get_room_name(self):
        raise NotImplementedError


class SeleniumTripPageParser(BaseTripPageParser):
    def __init__(self):
        # Set the options for Chrome driver
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, timeout=3)

    def parse(self, trip: Trip):
        self.driver.get(trip.url)

        is_available = self._check_availability()
        room_name = self._get_room_name()

        return is_available, room_name

    def _check_availability(self):
        try:
            trip_error_el = self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#bookItTripDetailsError")
                )
            )

            if trip_error_el and "dates" in trip_error_el.text:
                return False
        except TimeoutException:
            return True

    def _get_room_name(self):
        # Wait for the header element to be present on the page
        try:
            return self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            ).text
        except TimeoutException:
            raise Exception("Could not find room name")


# NOTE: for debug purposes, make sure to install ipython, which handles async execution
class PyppeteerTripPageParser(BaseTripPageParser):
    async def __init__(self, url):
        super().__init__(url)
        launch_options = {
            "headless": False,
        }
        self.browser = await launch(launch_options)
        self.page = await self.browser.newPage()
        await self.page.goto(self.url)

    async def check_availability(self):
        trip_error_el = await self.page.waitForSelector(
            "#bookItTripDetailsError", timeout=3000
        )

        if not trip_error_el:
            return True

        trip_error_text = await self.page.evaluate(
            "el => el.textContent", trip_error_el
        )

        if "dates" in trip_error_text:
            return False
        else:
            return True

    async def get_room_name(self):
        title_html = await self.page.waitForSelector("h1", timeout=3000)
        if title_html:
            return await self.page.evaluate("el => el.textContent", title_html)
        else:
            raise Exception("Could not find room name")

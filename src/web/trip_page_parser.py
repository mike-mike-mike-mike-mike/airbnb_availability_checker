from trip import Trip

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from pyppeteer import launch

from playwright.sync_api import sync_playwright


class TripPageParserFactory:
    class ParserType:
        SELENIUM = "selenium"
        PYPPETEER = "pyppeteer"
        PLAYWRIGHT = "playwright"

    @staticmethod
    def get_parser(type):
        if type == TripPageParserFactory.ParserType.SELENIUM:
            return SeleniumTripPageParser()
        elif type == TripPageParserFactory.ParserType.PYPPETEER:
            return PyppeteerTripPageParser()
        elif type == TripPageParserFactory.ParserType.PLAYWRIGHT:
            return PlaywrightTripPageParser()
        else:
            raise Exception("Invalid parser type")


class BaseTripPageParser:
    class AvailabilityException(Exception):
        """Exception raised when availxability status cannot be determined."""

        def __init__(self, message="Could not determine availability status"):
            super().__init__(message)

    def parse(self):
        raise NotImplementedError

    def close(self):
        pass

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

        room_name = self._get_room_name()
        is_available = self._check_availability()

        return is_available, room_name

    def _check_availability(self):
        # try:
        #     trip_error_el = self.wait.until(
        #         EC.presence_of_element_located(
        #             (By.CSS_SELECTOR, "#bookItTripDetailsError")
        #         )
        #     )

        #     if trip_error_el and "dates" in trip_error_el.text:
        #         return False
        # except TimeoutException:
        #     return True
        try:
            sidebar = self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div[data-section-id='BOOK_IT_SIDEBAR']")
                )
            )
            self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        ".//span[contains(text(), 'Reserve')] | .//*[@id='bookItTripDetailsError']",
                    )
                )
            )

            trip_error_els = sidebar.find_elements(
                By.CSS_SELECTOR, "#bookItTripDetailsError"
            )
            if trip_error_els and "dates" in trip_error_els[0].text:
                return False
            return True
        except TimeoutException:
            raise super().AvailabilityException()

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

    async def parse(self, trip: Trip):
        await self.page.goto(self.url)

        room_name = await self._get_room_name()
        is_available = await self._check_availability()

        return is_available, room_name

    async def close(self):
        await self.browser.close()

    async def _check_availability(self):
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

    async def _get_room_name(self):
        title_html = await self.page.waitForSelector("h1", timeout=3000)
        if title_html:
            return await self.page.evaluate("el => el.textContent", title_html)
        else:
            raise Exception("Could not find room name")


class PlaywrightTripPageParser(BaseTripPageParser):
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        self.page = self.browser.new_page()

    def parse(self, trip: Trip):
        self.page.goto(trip.url)

        room_name = self._get_room_name()
        is_available = self._check_availability()

        return is_available, room_name

    def close(self):
        self.browser.close()
        self.playwright.stop()

    def _check_availability(self):
        try:
            sidebar = self.page.wait_for_selector(
                "div[data-section-id='BOOK_IT_SIDEBAR']", timeout=3000
            )
            sidebar.wait_for_selector(
                "span:has-text('Reserve'), #bookItTripDetailsError", timeout=3000
            )

            trip_error_el = sidebar.query_selector("#bookItTripDetailsError")
            if trip_error_el and "dates" in trip_error_el.inner_text():
                return False
            return True
        except TimeoutError:
            raise super().AvailabilityException()

    def _get_room_name(self):
        try:
            header = self.page.wait_for_selector("h1", timeout=3000)
            return header.inner_text()
        except TimeoutError:
            raise Exception("Could not find room name")

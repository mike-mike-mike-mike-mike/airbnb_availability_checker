from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from functools import lru_cache

class TripPageParser:
    def __init__(self, url, driver=None):
        if driver:
            self.driver = driver
        else:
            # Set the options for Chrome driver
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            self.driver = webdriver.Chrome(options = options)

        self.url = url
        self.driver.get(self.url)
        self.wait = WebDriverWait(self.driver, timeout=3)

    @lru_cache(maxsize=None)
    def check_availability(self):
        # Wait for the element containing availability status to be present on the page
        try:
            element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#bookItTripDetailsError')))
            
            if element and 'Those dates are not available' in element.text:
                return False
        except TimeoutException:
            return True
        
    @lru_cache(maxsize=None)
    def get_room_name(self):
        # Wait for the header element to be present on the page
        try:
            return self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
        except TimeoutException:
            raise Exception('Could not find room name')

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

class AvailablityChecker:
    def __init__(self, url):
        self.driver = webdriver.Chrome()
        self.url = url

    def check_availability(self):
        self.driver.get(self.url)

        # Wait for the element containing availability status to be present on the page
        wait = WebDriverWait(self.driver, 4)
        try:
            element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#bookItTripDetailsError')))
            
            if element and 'Those dates are not available' in element.text:
                return False
        except TimeoutException:
            return True
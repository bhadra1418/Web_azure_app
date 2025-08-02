from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def login(self, email, password):    
        self.driver.find_element(By.NAME, "email").send_keys(email)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            print("Alert text:", alert.text)
            alert.accept()
        except TimeoutException:
            print("No alert appeared after login.")

        time.sleep(2)

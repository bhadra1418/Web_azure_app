from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def test_login_flow():
    driver = webdriver.Chrome()  # Ensure chromedriver is in PATH
    driver.get("http://127.0.0.1:5000/login")

    # Simulate login
    driver.find_element(By.NAME, "email").send_keys("demo@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("demo")
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

    time.sleep(2)
    assert "Invalid email or password" in driver.page_source

    driver.quit()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pytest

@pytest.fixture(scope="function")
def driver(request):
    # Set up Chrome options
   
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-features=PasswordCheck")
    chrome_options.add_argument("--disable-password-generation")
    chrome_options.add_argument("--disable-save-password-bubble")
    chrome_options.add_argument("--start-maximized")

    # Initialize driver
    service = Service()  # Let webdriver-manager auto-pick executable if configured
    driver = webdriver.Chrome(service=service, options=chrome_options)

    yield driver
    driver.quit()

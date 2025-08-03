from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from selenium.webdriver.common.by import By
import time
import pytest

@pytest.mark.usefixtures("driver")
def test_e2e_userflow_checkout(driver):
    driver.get("http://localhost:5000/login")
    login = LoginPage(driver)
    product_page = ProductsPage(driver)  # Correct class instantiation

    try:
        login.login("demo1@gmail.com", "demo1")
        welcome_text = driver.find_element(By.CLASS_NAME, "topbar").text
        assert "Welcome" in welcome_text
    except Exception as e:
        pytest.fail(f"Login failed: {e}")

    try:
        product_page.product_select()  # Correct method call
        cart_total = driver.find_element(By.CLASS_NAME, "cart-total")
        assert "₹799.0" in cart_total.text, "Cart total is incorrect"
    except Exception as e:
        pytest.fail(f"Checkout flow failed: {e}")

    
    try:
        #product_page.cart_remove()
        product_page.cart_checkout()
        time.sleep(3)
        success_message = driver.find_element(By.XPATH, "//p[contains(text(), 'order was placed successfully')]")
        assert success_message.is_displayed(), "Success message not displayed"
        print("Order success page verified") 
    except AssertionError:
        pytest.fail("Login failed or Products page not reached.")
    except Exception as e:
        pytest.fail(f"An unexpected error occurred: {e}")
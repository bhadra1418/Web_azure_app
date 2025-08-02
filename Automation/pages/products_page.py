from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class ProductsPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def product_select(self):
        # Click the Add to Cart button for USB-C Hub
        usb_c_hub_add_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@onclick, '/add_to_cart/3')]"))
        )
        usb_c_hub_add_button.click()

        # Wait for sidebar to be visible
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "sidebar")))

        # Wait for the USB-C Hub item to appear in the sidebar
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='cart-item']//strong[text()='USB-C Hub']"))
        )

    def cart_checkout(self):
        pay_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "pay-button")))
        pay_button.click()

    def cart_remove(self):
        short_wait = WebDriverWait(self.driver, 2)
        try:
            remove_button = short_wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "remove-button"))
            )
            if remove_button.is_displayed():
                remove_button.click()
                print("Item removed from cart.")
        except TimeoutException:
            print("Cart is already empty. No remove button found.")

    def verify_order_success(self):
        # Wait for the success message
        success_heading = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Thank you')]"))
        )
        success_message = self.driver.find_element(
            By.XPATH, "//p[contains(text(), 'order was placed successfully')]"
        )

        assert success_heading.is_displayed(), "Success heading not displayed"
        assert success_message.is_displayed(), "Success message not displayed"
        print("Order success page verified")

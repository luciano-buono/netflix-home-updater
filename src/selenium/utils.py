from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def handle_login(driver, email, password):
    try:
        # Attempt to find login elements
        email_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.NAME, "userLoginId"))
        )
        email_input.send_keys(email)

        password_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_input.send_keys(password)

        submit_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']"))
        )

        submit_button.click()
        # if login was needed, wait for the confirmation button
        confirmation_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[data-uia='set-primary-location-action']")
            )
        )
        confirmation_button.click()

    except TimeoutException:
        # Login elements not found, user is likely already logged in
        print("Login elements not found. Assuming user is already logged in.")
        # Proceed directly to the confirmation button
        confirmation_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[data-uia='set-primary-location-action']")
            )
        )
        confirmation_button.click()

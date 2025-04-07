import os
import pickle
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.constants import (
    NETFLIX_EMAIL,
    NETFLIX_PASSWORD,
    SELENIUM_REMOTE_URL,
    SELENIUM_USER_DATA_DIR,
    test_link,
)
from utils.logger import logger

COOKIE_FILE = "netflix_cookies.pkl"
REQUEST_WAIT_TIME = 2


def handle_confirm(driver):
    logger.info("Attempting to update household..")
    if element_present(driver, By.CSS_SELECTOR, "div[data-uia='upl-invalid-token']"):
        logger.warning("Link not valid. probably expired")
        return 1
    confirmation_button = WebDriverWait(driver, REQUEST_WAIT_TIME).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-uia='set-primary-location-action']"))
    )
    confirmation_button.click()
    logger.info("Household updated")


def element_present(driver, by, locator):
    try:
        WebDriverWait(driver, REQUEST_WAIT_TIME).until(EC.presence_of_element_located((by, locator)))
        return True
    except Exception:
        return False


def handle_login(driver, email, password):
    try:
        email_input = WebDriverWait(driver, REQUEST_WAIT_TIME).until(
            EC.presence_of_element_located((By.NAME, "userLoginId"))
        )
        email_input.send_keys(email)

        password_input = WebDriverWait(driver, REQUEST_WAIT_TIME).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_input.send_keys(password)

        submit_button = WebDriverWait(driver, REQUEST_WAIT_TIME).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']"))
        )

        # # Uncomment this to use user interaction to log in
        # WebDriverWait(driver, timeout=1000, poll_frequency=1) \
        # .until(EC.staleness_of(submit_button))

        submit_button.click()

    except TimeoutException:
        print("Login elements not found. Assuming user is already logged in.")
        confirmation_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-uia='set-primary-location-action']"))
        )
        confirmation_button.click()


def save_cookies(driver, filepath):
    with open(filepath, "wb") as f:
        pickle.dump(driver.get_cookies(), f)


def load_cookies(driver, filepath):
    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                driver.add_cookie(cookie)
        return True
    return False


def open_link_and_click(link):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument("--no-sandbox")  # Bypass OS security restrictions
    options.add_argument("--disable-dev-shm-usage")  # Prevent shared memory issues
    options.add_argument(f"--user-data-dir={SELENIUM_USER_DATA_DIR}")

    try:
        # Connect to Selenium WebDriver inside Docker
        driver = webdriver.Remote(command_executor=SELENIUM_REMOTE_URL, options=options)
        driver.get(link)
        if element_present(driver, By.NAME, "userLoginId"):
            logger.info("Attempting to log in to Netflix..")
            handle_login(driver, email=NETFLIX_EMAIL, password=NETFLIX_PASSWORD)
        handle_confirm(driver)
        time.sleep(10)  # Keep it open for VNC viewing
    finally:
        print("🛑 Closing browser...")
        driver.quit()


# Ensure the function runs only if the file is executed directly
if __name__ == "__main__":
    open_link_and_click(test_link)

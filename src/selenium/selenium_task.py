import time
import pickle
import os

from src.selenium.constants import NETFLIX_EMAIL, NETFLIX_PASSWORD

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from src.selenium.utils import handle_login
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


COOKIE_FILE = "netflix_cookies.pkl"


def handle_confirm(driver):
    confirmation_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[data-uia='set-primary-location-action']")
        )
    )
    confirmation_button.click()


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
    service = ChromeService(ChromeDriverManager().install())
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")

    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(link)

        if not load_cookies(driver, COOKIE_FILE):
            handle_login(driver, email=NETFLIX_EMAIL, password=NETFLIX_PASSWORD)
            save_cookies(driver, COOKIE_FILE)

        handle_confirm(driver)

    finally:
        driver.quit()


# Ensure the function runs only if the file is executed directly
if __name__ == "__main__":
    open_link_and_click()

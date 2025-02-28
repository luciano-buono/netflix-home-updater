import time

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from src.selenium.constants import NETFLIX_EMAIL, NETFLIX_PASSWORD
from src.selenium.utils import handle_login


def open_link_and_click(link):
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        driver.get(link)

        handle_login(driver, email=NETFLIX_EMAIL, password=NETFLIX_PASSWORD)

        time.sleep(60)

    finally:
        driver.quit()


# Ensure the function runs only if the file is executed directly
if __name__ == "__main__":
    open_link_and_click()

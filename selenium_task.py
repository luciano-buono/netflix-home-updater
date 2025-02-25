from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def open_link_and_click(link):
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    NETFLIX_EMAIL = "test"
    NETFLIX_PASSWORD = "test"

    

    try:
        driver.get(link)

        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "userLoginId"))
        )
        email_input.send_keys(NETFLIX_EMAIL)
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_input.send_keys(NETFLIX_PASSWORD)

        submit_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']"))
        )

        # submit_button.click()

        time.sleep(60)

        # inputs = driver.find_elements(By.TAG_NAME, "input")
        # for i, input_field in enumerate(inputs, start=1):
        #     print(f"Input {i}:")
        #     print(f"  Name: {input_field.get_attribute('name')}")
        #     print(f"  ID: {input_field.get_attribute('id')}")
        #     print(f"  Type: {input_field.get_attribute('type')}")
        #     print(f"  Placeholder: {input_field.get_attribute('placeholder')}")
        #     print("-" * 30)

        # button = driver.find_element(By.ID, "button_id")
        # button.click()
        # print("Button clicked successfully!")

    finally:
        driver.quit()

# Ensure the function runs only if the file is executed directly
if __name__ == "__main__":
    open_link_and_click()

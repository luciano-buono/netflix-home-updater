import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from utils.constants import SELENIUM_REMOTE_URL

# Setup Chrome options for VNC viewing
options = webdriver.ChromeOptions()
options.add_argument("--disable-dev-shm-usage")  # Fix crashes in Docker
options.add_argument("--no-sandbox")  # Required for Docker
# ❌ Do NOT use --headless, we need a visible browser for VNC


# options.add_argument("user-data-dir=selenium-cache/")
options.add_argument("--user-data-dir=/home/seluser/userdata")

# options.add_argument('--profile-directory=selenium-profile')


# Connect to the Selenium container
driver = webdriver.Remote(
    command_executor=SELENIUM_REMOTE_URL,
    options=options,
)

try:
    print("🚀 Opening Google...")
    driver.get("https://www.google.com")

    time.sleep(2)  # Wait for page to load

    print("🔍 Searching for 'Selenium'...")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("Selenium")
    search_box.send_keys(Keys.RETURN)

    time.sleep(50)  # Wait for results to appear

    print(f"✅ Page Title: {driver.title}")

finally:
    print("🛑 Closing browser...")
    driver.quit()

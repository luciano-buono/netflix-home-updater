import os

PORT = int(os.getenv("PORT", 8000))
NETFLIX_EMAIL = os.getenv("NETFLIX_EMAIL", "FILL")
NETFLIX_PASSWORD = os.getenv("NETFLIX_PASSWORD", "FILL")
SELENIUM_REMOTE_URL = os.getenv("SELENIUM_REMOTE_URL", "http://localhost:4444/wd/hub")
SELENIUM_USER_DATA_DIR = os.getenv("SELENIUM_USER_DATA_DIR", "/home/seluser/userdata")

test_link = os.getenv("test_link", "add-a-household-link-here")

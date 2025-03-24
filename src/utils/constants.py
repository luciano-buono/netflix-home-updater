import os

PORT = int(os.getenv("PORT", 8000))
NETFLIX_EMAIL = os.getenv("NETFLIX_EMAIL", "FILL")
NETFLIX_PASSWORD = os.getenv("NETFLIX_PASSWORD", "FILL")
SELENIUM_REMOTE_URL = os.getenv("SELENIUM_REMOTE_URL", "http://localhost:4444/wd/hub")
SELENIUM_USER_DATA_DIR = os.getenv("SELENIUM_USER_DATA_DIR", "/home/seluser/userdata")

test_link = (
    "https://www.netflix.com/account/update-primary-location?"
    "nftoken=BgjolOvcAxKkAbXjIkTxYiANxGkuLny44J0xNhg028uy5xutdsi0giQ62dVY"
    "IpKEWlxcgYempR1y6Dt2XvujuKRhElprB6qJTwRR8tfxRAE9VkcdfyKsBfcyN/LAjB2dH"
    "BC1nrc7MtnlBtlEJ/hcicNL4f1RKrxmAHOBz8GNeUmeHNiKn+j8qYrsqA155eKT8Y4lDdv"
    "8r4u32Vx5GwaJ6lVQugNfIYuZsn+4e6+kGAYiDgoMlrvzM8A6ZVr7uAAm&g=4802e319-e0"
    "6c-42e2-96bf-8408a3a10d9f&lnktrk=EVO&operation=update&lkid=UPDATE_HOUSEHOLD_REQUESTED_OTP_CTA"
)

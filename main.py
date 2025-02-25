from src.google.utils import gmail_authenticate
from src.selenium.selenium_task import open_link_and_click

from src.emails.utils import get_latest_email_link


if __name__ == "__main__":
    service = gmail_authenticate()

    link = get_latest_email_link(service)

    open_link_and_click(link)

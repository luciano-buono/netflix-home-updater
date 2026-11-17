import os
import re
from email import message_from_file
from email.message import Message

from utils.logger import logger

NETFLIX_LINK_START = ["https://www.netflix.com/account/update-primary", "https://www.netflix.com/account/set-primary"]
NETFLIX_LINK_RE = re.compile("(?:" + "|".join(re.escape(s) for s in NETFLIX_LINK_START) + r")[^\s<>\[\]\"]*")


def parse_email_from_file(file_path: str):
    """Read and parse an email file (.eml or raw format)."""
    if not os.path.exists(file_path):
        logger.info(f"❌ File not found: {file_path}")
        return

    # Open and parse the email
    with open(file_path, "r", encoding="utf-8") as file:
        email_message: Message = message_from_file(file)
        email_data = email_message.as_string()
        get_netflix_link(email_data)


def get_netflix_link(email_data):
    txt = email_data
    for dat in email_data.split("--xYzZY"):
        if 'Content-Disposition: form-data; name="text"' in dat:
            txt = dat.split('"text"', 1)[1]
            break

    # Links appear as <url> (Outlook-forwarded) or [url] (original Netflix text part).
    match = NETFLIX_LINK_RE.search(txt)
    if not match:
        logger.info(
            "Unable to parse the correct link in the Email. "
            "Maybe the search string is not correct anymore or the Email is not a update Email?"
        )
        raise ValueError("Netflix update link not found")
    return match.group(0)


if __name__ == "__main__":
    # Example Usage
    email_file_path = "sample_email.eml"  # Change this to your email file path
    parse_email_from_file(email_file_path)

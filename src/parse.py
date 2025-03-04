import os
from email import message_from_file
from email.message import Message

NETFLIX_LINK_START = ["https://www.netflix.com/account/update-primary", "https://www.netflix.com/account/set-primary"]


def parse_email_from_file(file_path: str):
    """Read and parse an email file (.eml or raw format)."""
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return

    # Open and parse the email
    with open(file_path, "r", encoding="utf-8") as file:
        email_message: Message = message_from_file(file)
        email_data = email_message.as_string()
        get_netflix_link(email_data)


def get_netflix_link(email_data):
    email_data = email_data.split("--xYzZY")
    for dat in email_data:
        if 'Content-Disposition: form-data; name="text"' in dat:
            txt = dat.split('"text"')[1]
            break

    for s in NETFLIX_LINK_START:
        idx_start = txt.find(s)
        if idx_start != -1:
            break
        if idx_start == -1:
            print(
                "Unable to parse the correct link in the Email. "
                "Maybe the search string is not correct anymore or the Email is not a update Email?"
            )

    update_link = txt[idx_start:-1]
    idx_end = update_link.find(">\n")
    update_link = update_link[0:idx_end]
    return update_link


if __name__ == "__main__":
    # Example Usage
    email_file_path = "sample_email.eml"  # Change this to your email file path
    parse_email_from_file(email_file_path)

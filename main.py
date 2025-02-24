from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64
import re
import os

# Gmail API Scopes
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def gmail_authenticate():
    """Authenticate and create Gmail API service."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)


def extract_specific_line(text, keyword):
    """Extract lines containing the specific keyword."""
    lines = text.splitlines()
    matching_lines = [line for line in lines if keyword in line]
    return matching_lines


def get_latest_email(service, user_id="me"):
    """Fetch the latest email and extract specific lines."""
    # List messages
    results = (
        service.users()
        .messages()
        .list(userId=user_id, maxResults=1, labelIds=["Label_3325193623226064180"])
        .execute()
    )
    messages = results.get("messages", [])

    if not messages:
        print("No emails found.")
        return

    print(messages)
    # Get the latest message
    msg_id = messages[0]["id"]
    msg = (
        service.users()
        .messages()
        .get(userId=user_id, id=msg_id, format="full")
        .execute()
    )

    print(msg.get('snippet'))
    # Decode the email body
    data = ""
    payload = msg.get("payload", {})
    if "body" in payload and "data" in payload["body"]:
        data = payload["body"]["data"]
    elif "parts" in payload:
        for part in payload["parts"]:
            if "body" in part and "data" in part["body"]:
                data = part["body"]["data"]
                break

    if data:
        email_body = base64.urlsafe_b64decode(data).decode("utf-8")

        # Extract lines with 'update-primary-location'
        keyword = "update-primary-location"
        matching_lines = extract_specific_line(email_body, keyword)

        if matching_lines:
            print("Lines containing 'update-primary-location':")
            for line in matching_lines:
                print(line)
        else:
            print("No matching lines found.")
    else:
        print("No email body found.")


if __name__ == "__main__":
    # Authenticate and create Gmail API service
    service = gmail_authenticate()

    # Get and print specific lines from the latest email
    get_latest_email(service)

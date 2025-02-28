from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64
from email import message_from_bytes
import re
import os
from bs4 import BeautifulSoup


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
    print('-----\n')
    # Get the latest message
    msg_id = messages[0]["id"]
    msg = (
        service.users()
        .messages()
        .get(userId=user_id, id=msg_id, format="raw")
        .execute()
    )
    # print(msg.get('snippet'))
    # # Decode the email body
    # data = ""
    # payload = msg.get("payload", {})
    # if "body" in payload and "data" in payload["body"]:
    #     data = payload["body"]["data"]
    # elif "parts" in payload:
    #     for part in payload["parts"]:
    #         if "body" in part and "data" in part["body"]:
    #             data = part["body"]["data"]
    #             break

    # Decode the raw email content
    raw_msg = base64.urlsafe_b64decode(msg['raw'].encode('ASCII'))
    
    # Parse email using email.parser
    email_message = message_from_bytes(raw_msg)
    return email_message

def process_email(email_body):
    # Extract lines with 'update-primary-location'
    keyword = "update-primary-location"
    matching_lines = extract_specific_line(email_body, keyword)

    if matching_lines:
        print("Lines containing 'update-primary-location':")
        for line in matching_lines:
            print(line)
    else:
        print("No matching lines found.")

def process_email2(email_message):
    # Parse email using email.parser
    # Extract headers
    subject = email_message['Subject']
    sender = email_message['From']
    date = email_message['Date']

    # Extract body (handling multipart emails)
    body = ""
    if email_message.is_multipart():
        for part in email_message.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if content_type == "text/plain" and "attachment" not in content_disposition:
                body = part.get_payload(decode=True).decode()
                break
    else:
        body = email_message.get_payload(decode=True).decode()

    # # Print extracted information
    # print(f"Subject: {subject}")
    # print(f"From: {sender}")
    # print(f"Date: {date}")
    # print("Body:\n", body)


if __name__ == "__main__":
    # Authenticate and create Gmail API service
    service = gmail_authenticate()

    # Get and print specific lines from the latest email
    email_body = get_latest_email(service)
    # process_email(email_body=email_body)
    process_email2(email_message=email_body)


import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def list_messages(service):
    """List Gmail messages."""
    try:
        results = service.users().messages().list(userId='me', labelIds=['Label_3325193623226064180']).execute()
        messages = results.get('messages', [])

        if not messages:
            print('No new messages.')
        else:
            print(f'Found {len(messages)} new message(s).')
            for message in messages[:5]:  # Limiting to first 5 unread messages
                msg = service.users().messages().get(userId='me', id=message['id']).execute()
                print(f"Subject: {msg['payload']['headers'][0]['value']}")
                print(f"From: {msg['payload']['headers'][1]['value']}")
                print(f"From: {msg['payload']['body']}")
                print("-" * 50)

    except HttpError as error:
        print(f'An error occurred: {error}')

def main():
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
    results = service.users().labels().list(userId="me").execute()
    labels = results.get("labels", [])

    if not labels:
      print("No labels found.")
      return
    print("Labels:")
    for label in labels:
      print(label["name"])

    list_messages(service=service)

  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()



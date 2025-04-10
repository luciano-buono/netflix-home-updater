import base64
import re

EMAIL_LABEL_NETFLIX = "Label_3325193623226064180"


def extract_specific_line(text, keyword):
    lines = text.splitlines()
    matching_lines = [line for line in lines if keyword in line]
    return matching_lines


def get_emails_by_label(service, label, user_id="me"):
    results = (
        service.users()
        .messages()
        .list(
            userId=user_id,
            maxResults=1,
            labelIds=[label],
        )
        .execute()
    )
    messages = results.get("messages", [])

    if not messages:
        print("No emails found.")
        return

    return messages


def get_labels(service, user_id="me"):
    results = service.users().labels().list(userId=user_id).execute()
    labels = results.get("labels", [])

    if not labels:
        print("No labels found.")
        return

    for label in labels:
        print(f"ID: {label['id']}, Name: {label['name']}")

    return labels


def get_latest_email_link(service, user_id="me"):
    messages = get_emails_by_label(service, EMAIL_LABEL_NETFLIX, user_id)

    msg_id = messages[0]["id"]
    msg = service.users().messages().get(userId=user_id, id=msg_id, format="full").execute()

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

        keyword = "update-primary-location"
        matching_lines = extract_specific_line(email_body, keyword)

        if matching_lines:
            for line in matching_lines:
                match = re.search(r"<(https?://[^>]+)>", line)
                return match.group(1)
        else:
            print("No matching lines found.")
    else:
        print("No email body found.")

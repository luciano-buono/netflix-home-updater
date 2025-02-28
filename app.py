from fastapi import FastAPI, Request, Form
from typing import Optional
from pydantic import BaseModel
from typing import Dict
import json
from sendgrid.helpers.inbound.parse import Parse
from email import message_from_bytes
from email.message import Message

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

@app.post("/webhook/")
async def webhook(request: Request):
    """Receive raw email from SendGrid and extract plain text & HTML content."""
    raw_email = await request.body()  # Get the raw email bytes
    email_message: Message = message_from_bytes(raw_email)  # Parse email content

    # Extract headers
    from_email = email_message.get("From")
    to_email = email_message.get("To")
    subject = email_message.get("Subject")

    print("📩 New Email Received:")
    print(f"From: {from_email}")
    print(f"To: {to_email}")
    print(f"Subject: {subject}")

    # Initialize body containers
    text_body, html_body = None, None

    # Extract email content (text & HTML)
    if email_message.is_multipart():
        for part in email_message.walk():
            content_type = part.get_content_type()
            content_disposition = part.get("Content-Disposition")

            # Extract plain text body
            if content_type == "text/plain" and "attachment" not in str(content_disposition):
                text_body = part.get_payload(decode=True).decode(errors="ignore")

            # Extract HTML body
            elif content_type == "text/html" and "attachment" not in str(content_disposition):
                html_body = part.get_payload(decode=True).decode(errors="ignore")

    else:
        # If email is not multipart, extract the payload directly
        content_type = email_message.get_content_type()
        if content_type == "text/plain":
            text_body = email_message.get_payload(decode=True).decode(errors="ignore")
            email_data = email_message.as_string().split("--xYzZY")

            for dat in email_data:
                if "Content-Disposition: form-data; name=\"text\"" in dat:
                    txt = dat.split('"text"')[1]
                    print(txt)
        elif content_type == "text/html":
            html_body = email_message.get_payload(decode=True).decode(errors="ignore")

    # # Print extracted bodies
    # if text_body:
    #     print("\n📜 Email Body (Text):")
    #     print(text_body)

    # if html_body:
    #     print("\n🖥️ Email Body (HTML):")
    #     print(html_body)

    return {"message": "Email processed successfully", "from": from_email, "subject": subject}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)



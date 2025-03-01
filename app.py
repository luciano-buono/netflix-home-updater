from fastapi import FastAPI, Request
from email import message_from_bytes
from email.message import Message

from parse import get_netflix_link

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}


@app.post("/webhook/")
async def webhook(request: Request):
    """Receive raw email from SendGrid and extract plain text & HTML content."""
    raw_email = await request.body()  # Get the raw email bytes
    email_message: Message = message_from_bytes(raw_email)  # Parse email content

    # Extract email content (text & HTML)
    if email_message.is_multipart():
        for part in email_message.walk():
            content_type = part.get_content_type()
            content_disposition = part.get("Content-Disposition")

            # Extract plain text body
            if content_type == "text/plain" and "attachment" not in str(
                content_disposition
            ):
                email_data = part.as_string()
    else:
        # If email is not multipart, extract the payload directly
        content_type = email_message.get_content_type()
        if content_type == "text/plain":
            email_data = email_message.as_string()

    link = get_netflix_link(email_data=email_data)
    print(link)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)

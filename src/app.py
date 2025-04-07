from email import message_from_bytes
from email.message import Message

import uvicorn
from fastapi import FastAPI, HTTPException, Request

from parse import get_netflix_link
from selenium_utils.selenium_task import open_link_and_click
from utils.constants import PORT, SELENIUM_USER_DATA_DIR
from utils.logger import logger

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}


@app.get("/readyz/")
@app.get("/health/")
@app.get("/livez/")
def livez():
    return {"message": "ok"}


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
            if content_type == "text/plain" and "attachment" not in str(content_disposition):
                email_data = part.as_string()
    else:
        # If email is not multipart, extract the payload directly
        content_type = email_message.get_content_type()
        if content_type == "text/plain":
            email_data = email_message.as_string()
    try:
        link = get_netflix_link(email_data=email_data)
        logger.info(f"Link parsed from 📧: {link}")
        open_link_and_click(link)
    except Exception:
        raise HTTPException(status_code=404, detail="Parse link error")


if __name__ == "__main__":
    logger.info(f"Start listening on PORT:{PORT}")
    logger.info(f"Using selenium user data dir: {SELENIUM_USER_DATA_DIR}")
    uvicorn.run("app:app", port=PORT, reload=True, host="0.0.0.0")

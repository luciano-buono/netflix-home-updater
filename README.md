![alt text](_docs/diagram.drawio.png)

## Install

```bash
uv init .
uv pip install
```


## Components
- Outlook forward rule (or any mail that allows to creates forward rules using recipient and subjects)
- Domain and ability to create MX record for it
- Sendgrid account using Inbound parse webhook
- FastAPI webserver listening for POST requests
- Selenium parsing HTML and clicking on Netflix button
- Selenium standalone-chromium container



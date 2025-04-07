![alt text](_docs/diagram.drawio.png)

## Components
- Outlook forward rule (or any mail that allows to creates forward rules using recipient and subjects)
- Domain and ability to create MX record for it
- Sendgrid account using [Inbound parse webhook](https://www.twilio.com/docs/sendgrid/for-developers/parsing-email/setting-up-the-inbound-parse-webhook)
- FastAPI webserver listening for POST requests
- Selenium parsing HTML and clicking on Netflix button
- Selenium standalone-chromium container

## Contributors:
- [@julio-jg](https://github.com/juliojg)

## Install with docker

```bash
docker compose build
docker compuse up -d

```

Compose uses 2 containers, one with webserver and second one with standalone selenium.
We decided on this because selenium does not have a lot of support in ARM64 architectures using the local browser inside the same webserver.
More info here: https://github.com/SeleniumHQ/docker-selenium#browser-images-in-multi-arch

## Local development

```bash
uv init .
uv pip install
```

## Setup

1. Define the email you want to use for the webhook. For example, if you domain is domain.com, you can use:
  - info@netflix-checker.domain.com
2. Add a rule in your real email where you receive Netflix Household updates in which you forward the emails from "info@account.netflix.com" <info@account.netflix.com> to your webkook email.
 - You can further filter this by only sending emails based on specific subjects
3. In your Sendgrid/Twilio account, set up an Inbound parse webhook using the email defined above and selecting your server URL, for example:
  - netflix-home-updater.k3s.domain.com
  - You will also need to add MX records in your domain in order to allow Sendgrid to process this emails (Check docs for setup)[1](https://www.twilio.com/docs/sendgrid/for-developers/parsing-email/setting-up-the-inbound-parse-webhook)
4. Start your webserver, define your netflix user/password as `NETFLIX_EMAIL` `NETFLIX_PASSWORD` inside env vars.

If using K8s/docker remember to persist the `SELENIUM_USER_DATA_DIR` folder, so the browser won't need to login into Netflix each time the workflow is ran.

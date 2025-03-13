ARG ENVIRONMENT
FROM python:3.13-slim
ENV ENVIRONMENT=${ENVIRONMENT:-development}

# Install dependencies
RUN apt-get update && apt-get install -y \
  wget unzip curl vim \
  chromium chromium-driver

COPY requirements/$ENVIRONMENT.txt /app/requirements.txt
# Install Selenium
RUN pip install -r /app/requirements.txt

RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid 1001 appuser

USER 1001
# Set environment variables

ENV DISPLAY=:99

# Copy app files
COPY --chown=1001:1001 ./src/ /app
WORKDIR /app

CMD ["python", "app.py"]

ARG ENVIRONMENT
FROM python:3.13-slim
ENV ENVIRONMENT=${ENVIRONMENT:-development}

# Install dependencies
RUN apt-get update && apt-get install -y \
  wget unzip curl \
  chromium chromium-driver

COPY requirements/$ENVIRONMENT.txt /app/requirements.txt
# Install Selenium
RUN pip install -r /app/requirements.txt
# Set environment variables
ENV DISPLAY=:99

# Copy app files
COPY ./src/ /app
WORKDIR /app

CMD ["python", "app.py"]

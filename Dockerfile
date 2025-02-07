# Use Python 3.12-slim as the base
FROM python:3.12-slim

# Install Google Chrome Stable (official repo) + required packages
RUN apt-get update && apt-get install -y \
    wget gnupg2 libnss3 libgconf-2-4 libxi6 libgbm1 curl unzip \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" \
       > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Set the work directory
WORKDIR /app

# Upgrade pip and install Poetry
RUN pip install --upgrade pip && pip install poetry

# Copy and install dependencies
COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-root

# Copy cookies.json (if needed)
COPY cookies.json /app/

# Copy source code + environment
COPY src /app/src
COPY .env /app/

# Create a directory for the database
RUN mkdir -p /app/db

# Expose the Flask port
EXPOSE ${APP_PORT}

# Run the Flask app
CMD ["poetry", "run", "python", "src/server.py"]

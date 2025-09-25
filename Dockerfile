# syntax=docker/dockerfile:1
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    supervisor \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

# Django specific setup
# Use the full path to manage.py and the venv's python
RUN /usr/local/bin/python manage.py makemigrations api_admin
RUN /usr/local/bin/python manage.py migrate
RUN /usr/local/bin/python manage.py collectstatic --noinput

# Create log directory for Supervisor
RUN mkdir -p /app/logs

EXPOSE 8000 8001

# Supervisor will manage both FastAPI and Django processes
# Copy the Supervisor config file to the correct location for Supervisor
COPY metalworkers-api.conf /etc/supervisor/conf.d/metalworkers-api.conf

# Copy and make the startup script executable
COPY start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh

# Set the entrypoint to our startup script
ENTRYPOINT ["/usr/local/bin/start.sh"]

# Default command to run if no arguments are provided to docker run
CMD ["bash"] 
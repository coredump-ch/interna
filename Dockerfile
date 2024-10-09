# Docker image for Interna.
#
# Please set the following env vars:
#
# - SECRET_KEY=...
# - DATABASE_URL='postgres://<postgres-host>/<database-name>'
# - SITE_DOMAIN='https://<domain>[:<port>]'
# - ALLOWED_HOST='<domain>'
# - SMTP_HOST=...
# - SMTP_PORT=...
# - SMTP_USER=...
# - SMTP_PASS=...
#
# See docker-compose.yml as an example on how to run this image.

FROM docker.io/python:3.13-slim-bullseye

# Add requirements file
ADD requirements.txt /code/requirements.txt
WORKDIR /code

# Install dependencies
RUN apt-get update -qq \
 && apt-get install -yq --no-install-recommends \
    dumb-init \
 && rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt

# Add code
ADD . /code

# Set env vars
ENV DJANGO_DEBUG=False

# Volumes
VOLUME ["/code/interna/static/", "/code/interna/media/"]

# Entry point
ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["/bin/bash", "entrypoint.sh"]

#!/usr/bin/env bash
#
# Entry point script for Docker
set -euo pipefail

if [ -z "${SECRET_KEY:-}" ]; then
    echo 'Error: Missing SECRET_KEY env variable.'
    echo 'You can generate a secret key with `openssl rand -hex 32`.'
    exit 1
fi
if [ -z "${DATABASE_URL:-}" ]; then
    echo 'Error: Missing DATABASE_URL env variable.'
    exit 1
fi
if [ -z "${SITE_DOMAIN:-}" ]; then
    echo 'Error: Missing SITE_DOMAIN env variable.'
    exit 1
fi
if [ -z "${SMTP_HOST:-}" ] || [ -z "${SMTP_USER:-}" ] || [ -z "${SMTP_PASS:-}" ] || [ -z "${SMTP_PORT:-}" ]; then
    echo 'Error: Missing SMTP_* env variables.'
    exit 1
fi

cd interna

# We need to wait for the database to be ready until we can run migrations.
# To do this, retry up to 15 times to run the migrations. Once that worked,
# we can assume that the database is up and ready.
success=0
retries=15
for i in $(seq $retries); do
    echo "Running migrations…"
    ./manage.py migrate && success=1 && break || true
    echo "Database not yet ready, waiting ($i/$retries)…"
    sleep 1
done
if [ "$success" -eq 1 ]; then
    echo "Database is up, all migrations applied"
else
    echo "Timed out waiting for database"
    exit 1
fi

echo "Create cache table…"
./manage.py createcachetable

echo "Collect static files…"
./manage.py collectstatic

echo "Start server…"
gunicorn config.wsgi:application \
    -n interna \
    -b 0.0.0.0:8000 \
    -w 4 \
    --access-logfile - \
    --error-logfile - \
    --log-level info

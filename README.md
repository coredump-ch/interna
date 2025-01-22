# Coredump Interna

[![Build Status](https://github.com/coredump-ch/interna/workflows/CI/badge.svg)](https://github.com/coredump-ch/interna/actions?query=branch%3Amaster)

Interne Platform für Mitgliederverwaltung etc...

Docker image: <https://hub.docker.com/r/coredump/interna>


## API

Es besteht eine API zum Abfragen der aktiven Mitglieder:

- https://interna.coredump.ch/api/members/active/ (GET)

Für die Authentisierung wird ein Session Cookie oder Basic Auth akzeptiert.


## Dev setup

Voraussetzungen:

- Python 3
- Docker

Container mit PostgreSQL starten:

    docker run -d --name interna-pg \
      -e POSTGRES_DB=interna \
      -e POSTGRES_USER=interna \
      -e POSTGRES_PASSWORD=interna-dev-password \
      -p 127.0.0.1:5432:5432 docker.io/postgres:14-alpine

[Virtualenv](https://docs.python.org/3/library/venv.html) erstellen:

    python3 -m venv VENV
    source VENV/bin/activate

Abhängigkeiten installieren:

    pip install -r requirements.txt

In Source-Directory wechseln:

    cd interna

Umgebungsvariablen definieren (`.env` Datei wird automatisch geladen):

    echo "DJANGO_DEBUG=True" >> .env
    echo "SITE_DOMAIN='http://localhost:8000'" >> .env
    echo "DATABASE_URL='postgres://interna:interna-dev-password@localhost/interna'" >> .env

Datenbank migrieren:

    ./manage.py migrate
    ./manage.py createcachetable

Tests laufen lassen:

    pytest

User erstellen:

    ./manage.py createsuperuser

Testdaten laden (optional):

    ./manage.py loaddata --app crowdfund testdata
    ./manage.py loaddata --app memberdb testdata

Entwicklungsserver starten:

    ./manage.py runserver

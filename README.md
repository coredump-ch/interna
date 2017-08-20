Coredump Interna
================

[![Build Status](https://travis-ci.org/coredump-ch/interna.png?branch=master)](https://travis-ci.org/coredump-ch/interna)

Interne Platform für Mitgliederverwaltung etc...

Dev setup
---------

Voraussetzungen:

- Python 3
- Pip
- Virtualenvwrapper
- PostgreSQL

Datenbank:

    createdb interna

Abhängigkeiten installieren:

    mkvirtualenv interna
    pip install -r requirements.txt

In Source-Directory wechseln:

    cd interna

Umgebungsvariablen definieren (`.env` Datei wird automatisch geladen):

    echo "DJANGO_DEBUG=True" >> .env
    echo "SITE_DOMAIN='http://localhost:8000'" >> .env
    echo "DATABASE_URL='postgres://localhost/interna'" >> .env

Datenbank migrieren:

    ./manage.py migrate

Entwicklungsserver starten:

    ./manage.py runserver

Tests laufen lassen:

    ./runtests.py

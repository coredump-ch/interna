Coredump Interna
================

[![Build Status](https://travis-ci.org/coredump-ch/interna.png?branch=master)](https://travis-ci.org/coredump-ch/interna)

Interne Platform für Mitgliederverwaltung etc...

Dev setup
---------

Voraussetzungen:

- Python 3
- Pip
- PostgreSQL

Datenbank:

    createdb interna

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
    echo "DATABASE_URL='postgres://localhost/interna'" >> .env

Datenbank migrieren:

    ./manage.py makemigrations thumbnail  # Workaround: https://stackoverflow.com/a/35883910/284318
    ./manage.py migrate

Tests laufen lassen:

    ./runtests.py

User erstellen:

    ./manage.py createsuperuser

Testdaten laden (optional):

    ./manage.py loaddata --app crowdfund testdata

Entwicklungsserver starten:

    ./manage.py runserver

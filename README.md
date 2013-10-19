Coredump Interna
================

[![Build Status](https://travis-ci.org/coredump-ch/interna.png?branch=master)](https://travis-ci.org/coredump-ch/interna)

Interne Platform für Mitgliederverwaltung etc...

Dev setup
---------

Voraussetzungen:

- Python 2.7+
- Pip
- Virtualenvwrapper
- PostgreSQL

Datenbank::

    createdb interna

Abhängigkeiten installieren::

    mkvirtualenv interna
    pip install -r requirements.txt

Umgebungsvariablen definieren::

    POSTACTIVATE=$VIRTUAL_ENV/$VIRTUALENVWRAPPER_ENV_BIN_DIR/postactivate
    echo "export DJANGO_DEBUG=True" >> $POSTACTIVATE
    echo "export PORT=8000" >> $POSTACTIVATE
    echo "export SITE_DOMAIN='http://localhost:8000'" >> $POSTACTIVATE
    echo "export DATABASE_URL='postgres://localhost/interna'" >> $POSTACTIVATE
    source $POSTACTIVATE

Datenbankschema generieren::

    cd interna
    ./manage.py syncdb
    ./manage.py migrate

Entwicklungsserver starten::

    ./manage.py runserver

#! /bin/bash

python -m venv .venv

python -m pip install --upgrade pip

.venv/bin/pip install mysqlclient==2.1.0
.venv/bin/pip install -r requirements.txt

.venv/bin/python manage.py migrate
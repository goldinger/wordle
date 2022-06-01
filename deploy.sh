#! /bin/bash

# if venv doesn't exist, create it
if [ ! -d ".venv" ]; then
    python -m venv .venv
fi

.venv/bin/pip install -r requirements.txt
.venv/bin/python manage.py migrate
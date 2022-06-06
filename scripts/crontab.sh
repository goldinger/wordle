#! /bin/sh

. .venv/bin/activate

python manage.py crontab remove
python manage.py crontab add
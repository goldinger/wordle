#!/bin/sh

if [ -d ".venv" ] 
then
    echo "Python virtual environment exists." 
else
    ~/.pyenv/versions/3.9.13/bin/python3 -m venv env
fi

. .venv/bin/activate

pip install -r requirements.txt

if [ -d "logs" ] 
then
    echo "Log folder exists." 
else
    mkdir logs
    touch logs/error.log logs/access.log
fi

sudo chmod -R 777 logs
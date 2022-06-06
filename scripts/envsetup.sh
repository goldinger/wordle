#!/bin/sh

if [ -d ".venv" ] 
then
    echo "Python virtual environment exists." 
else
    ~/.pyenv/versions/3.9.13/bin/python3 -m venv .venv
fi

. .venv/bin/activate

python --version

python -m pip install --upgrade pip

pip install -r requirements.txt

if [ -d "logs" ] 
then
    echo "Log folder exists." 
else
    mkdir logs
fi

sudo chmod -R 777 logs
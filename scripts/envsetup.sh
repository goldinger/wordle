#!/bin/sh

if [ -d ".venv" ] 
then
    echo "Python virtual environment exists." 
else
    ~/.pyenv/versions/3.9.13/bin/python3 -m venv .venv
fi

. .venv/bin/activate

python --version

python -m pip install --upgrade pip wheel setuptools

pip install mysqlclient==2.1.0
pip install gunicorn==20.1.0
pip install -r requirements.txt

if [ -f "chromedriver"]
then
    echo "Chromedriver exists"
else
    sudo apt install -y unzip
    wget https://chromedriver.storage.googleapis.com/103.0.5060.24/chromedriver_linux64.zip
    unzip chromedriver_linux64.zip
fi

if [ -d "logs" ] 
then
    echo "Log folder exists." 
else
    mkdir logs
fi

sudo chmod -R 777 logs
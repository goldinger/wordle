#!/bin/sh

sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
sudo echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list

sudo apt update
sudo apt install -y curl unzip xvfb libxi6 libgconf-2-4 default-jdk google-chrome-stable


wget https://chromedriver.storage.googleapis.com/103.0.5060.24/chromedriver_linux64.zip
unzip chromedriver_linux64.zip

sudo mv chromedriver /usr/bin/chromedriver
sudo chown jenkins:jenkins /usr/bin/chromedriver
sudo chmod +x /usr/bin/chromedriver
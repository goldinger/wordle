#!/bin/sh

sudo systemctl daemon-reload

sudo systemctl start wordle

echo "Gunicorn has started."

sudo systemctl enable wordle

echo "Gunicorn has been enabled."

sudo systemctl restart wordle

sudo systemctl status wordle
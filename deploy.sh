# if venv doesn't exist, create it
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# activate virtualenv
source venv/bin/activate
pip install -r requirements.txt
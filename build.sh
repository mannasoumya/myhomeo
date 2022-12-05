set -xe
python3.9 -m venv venv
. ./venv/bin/activate
pip install pip-tools
pip-compile -o requirements.txt requirements.in
pip install -r requirements.txt

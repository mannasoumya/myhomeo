set -xe
python3 -m venv venv
. ./venv/bin/activate
pip install pip-tools
pip-compile -o requirements.txt requirements.in
pip install -r requirements.txt

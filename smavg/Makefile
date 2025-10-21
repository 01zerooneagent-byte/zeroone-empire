.PHONY: run update install deploy clean live-update
install:
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
update:
.venv/bin/python scripts/update.py
run:
.venv/bin/python web/app.py
deploy: install update run
live-update:
.venv/bin/python scripts/update.py
clean:
rm -rf .venv data/state.json data/metrics.json
reset:
rm -rf data/*.json

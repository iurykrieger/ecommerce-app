.PHONY: install run

install:
	python3 -m venv venv; \
	. venv/bin/activate; \
	pip install -r requirements.txt;

run:
	FLASK_APP=src/main.py flask run
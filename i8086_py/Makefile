.PHONY: test install dev venv
.ONESHELL:

test:
	. .venv/bin/activate
	python3.12 -m unittest discover

install:
	test -d .venv || python3.12 -m venv .venv
	. .venv/bin/activate
	python3.12 -m pip install -U pip setuptools wheel
	python3.12 -m pip install .

dev:
	test -d .venv || python3.12 -m venv .venv
	. .venv/bin/activate
	python3.12 -m pip install -U pip setuptools wheel
	python3.12 -m pip install -e .[dev]

clean:
	rm -rf .venv
	find -iname "*.pyc" -delete

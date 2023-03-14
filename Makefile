SHELL := /bin/bash
WORKDIR := .
ENVDIR := $(WORKDIR)/.env
ENV := $(ENVDIR)/bin
ACTIVATE := . $(ENV)/activate

.PHONY: install
install: requirements.txt
	$(ENV)/pip install -U pip
	$(ENV)/pip install -Ur requirements.txt

.PHONY: env
env:
	$(ACTIVATE)

.PHONY: lint
lint: env
	$(ENV)/pylint src/ setup.py --reports=y > reports/pylint.report

.PHONY: test
test: env
	$(ENV)/coverage run --source="." ./src/manage.py test --settings=settings.testing
	$(ENV)/coverage report
	$(ENV)/coverage html

.PHONY: messages
messages: env
	$(ENV)/python manage.py makemessages -l de
	$(ENV)/python manage.py makemessages -l es
	$(ENV)/python manage.py compilemessages -l de
	$(ENV)/python manage.py compilemessages -l es

.PHONY: clean
clean:
	rm -rf __pycache__
	rm -rf venv

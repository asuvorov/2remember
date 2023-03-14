SHELL := /bin/bash

install:
	@pip install -U pip && pip install -r requirements.txt

env:
	@source .env/bin/activate

lint:
	@pylint src/ setup.py --reports=y > reports/pylint.report

test:
	@coverage run --source="." ./src/manage.py test --settings=settings.testing
	@coverage report
	@coverage html

env:
	@source .env/bin/activate

lint:
	@pylint src/ setup.py --reports=y > reports/pylint.report

test:
	@coverage run --source="." ./src/manage.py test --settings=settings.testing
	@coverage report
	@coverage html

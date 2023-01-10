env:
	@source .env/bin/activate

lint:
	@pylint src/ setup.py --reports=y > reports/pylint.report

SHELL = /bin/bash
env:
	@echo $(info $(SHELL))
	@source .env/bin/activate

lint:
	@pylint src/ setup.py --reports=y > reports/pylint.report

test: env
	@coverage run --source="." ./src/manage.py test --settings=settings.testing
	@coverage report
	@coverage html

messages: env
	@python src/manage.py makemessages    -l de
	@python src/manage.py makemessages    -l es
	@python src/manage.py compilemessages -l de
	@python src/manage.py compilemessages -l es

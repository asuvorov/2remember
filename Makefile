SHELL = /bin/bash
ACTIVATE := . .env/bin/activate

.PHONY: env
env:
	$(ACTIVATE)

.PHONY: lint
lint:
	@pylint src/ setup.py --reports=y > reports/pylint.report

.PHONY: test
test: env
	@coverage run --source="." ./src/manage.py test --settings=settings.testing
	@coverage report
	@coverage html

.PHONY: messages
messages: env
	$(ACTIVATE) && cd src/ && python manage.py makemessages -l de && python manage.py makemessages -l es && python manage.py compilemessages -l de &&python manage.py compilemessages -l es

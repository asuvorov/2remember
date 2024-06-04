.DEFAULT_GOAL := help

SHELL := /bin/bash
WORKDIR := .
ENVDIR := $(WORKDIR)/.env
ENV := $(ENVDIR)/bin
ACTIVATE := . $(ENV)/activate

COMPOSE_SERVICE_NAME := "web"

# =============================================================================
# === Set-up Targets.
# =============================================================================
##@ Set-up
setup: ## Initiate Virtual Environment.
	$(info Initiating Virtual Environment)
	@virtualenv .env
.PHONY: setup

env: setup ## Activate Virtual Environment.
	$(info Activating Virtual Environment)
	$(ACTIVATE)
.PHONY: env

# =============================================================================
# === Development Targets.
# =============================================================================
##@ Development
install: env requirements.txt ## Install Requirements.
	$(info Installing Requirements)
	$(ENV)/pip install -U  pip
	$(ENV)/pip install -Ur requirements.txt --no-cache-dir
.PHONY: install

test: install ## Run Tests.
	$(info Running Tests)
	$(ENV)/coverage run --source="." ./src/manage.py test --settings=settings.testing
	$(ENV)/coverage report -m --skip-empty
	$(ENV)/coverage html --skip-empty
.PHONY: test

test-local: build-local ## Run Tests.
	$(info Running Tests)
	@docker-compose -f docker-compose.yml -f docker-compose.test.yml run --rm --user $(UID):`id -g` web coverage run --source="." ./manage.py test --settings=settings.testing && coverage report -m --skip-empty && coverage html --skip-empty
	# @docker-compose -f docker-compose.yml -f docker-compose.test.yml run --rm --user $(UID):`id -g` web python -m pytest --pylint --junitxml=test-output.xml --cov-report term --cov-report xml:cov.xml --cov=bnetcontentcore tests/unit
.PHONY: test-local

apitest: install ## Run API Tests.
	$(info Running API Tests)
.PHONY: apitest

apitest-local: install ## Run API Tests on local.
	$(info Running API Tests)
.PHONY: apitest-local

lint: install ## Run Linter.
	$(info Running Linter)
	$(ENV)/pylint src/ setup.py --reports=y > reports/pylint.report
.PHONY: lint

# =============================================================================
# === Clean-up Targets.
# =============================================================================
##@ Clean-up
mostly-clean: ## Stop/remove all the locally created Containers, and Volumes.
	$(info Cleaning up Things)
	@docker-compose down --rmi local -v --remove-orphans
.PHONY: mostly-clean

clean: mostly-clean ## Stop/remove all the locally built Images, Containers, and Volumes; clean up the Project Folders.
	$(info Cleaning up Things)
	@rm -rf __pycache__
	@rm -rf *.pyc
	@rm -rf .env
.PHONY: clean

prune: clean ## Do a System Prune to remove untagged and unused Images/Containers.
	$(info Doing a System Prune)
	@docker system prune -af
	@docker volume prune -af
.PHONY: prune

# =============================================================================
# === Documentation Targets.
# =============================================================================
##@ Documentation
swagger-build: ## Build Swagger Image.
	@cd ./swagger; ./view_or_edit_swagger.sh

swagger-view: ## Run Swagger in the view Mode.
	@cd ./swagger; ./view_or_edit_swagger.sh view

swagger-edit: ## Run Swagger in the edit Mode.
	cd ./swagger; ./view_or_edit_swagger.sh edit

# =============================================================================
# === CI/CD Targets.
# =============================================================================
##@ CI/CD
login: ## Login the Docker Daemon to AWS ECR.
	$(info Logging the Docker Daemon to AWS ECR.)
.PHONY: login

build: login ## Build the Containers/Images, defined in the `docker-compose`.
	$(info Building the Containers/Images)
	@docker-compose -f docker-compose.yml build --no-cache --force-rm --pull $(COMPOSE_SERVICE_NAME)
	@docker-compose -f docker-compose.yml --compatibility up --no-start
.PHONY: build

build-local: login ## Build the Containers/Images, defined in the `docker-compose`, with a local Overrides.
	$(info Building the Containers/Images with a local Overrides)
	@docker-compose -f docker-compose.yml -f docker-compose.local.yml build
	@docker-compose up --no-start
.PHONY: build-local

run: login build run-local ## Start the `docker-compose`, that includes local `docker-compose` Overrides.

run-local: ## Start the Compose, bypassing Build Steps.
	$(info Starting the Compose)
	@docker-compose -f docker-compose.yml -f docker-compose.local.yml up -d
	@docker-compose -f docker-compose.yml -f docker-compose.local.yml exec web python manage.py migrate
# 	@docker-compose -f docker-compose.yml -f docker-compose.local.yml exec web python manage.py loaddata initial_data
.PHONY: run-local

down: ## Clean up the Project Folders.
	$(info Cleaning up Things)
	@docker-compose down
.PHONY: down

tag: ## Tag Images with the default or passed in `REPO` and `TAG` Arguments.
	$(info Tagging Images)
.PHONY: tag

publish: ## Publish a Package, such as a Python PIP Package.
	$(info Publishing a Package)
.PHONY: publish

push: login ## Push the tagged Images to the respective Repo.
	$(info Pushing the tagged Images to the respective Repo)
.PHONY: push

# =============================================================================
# === Helpers Targets.
# =============================================================================
##@ Helpers
help: ## Display this Help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
.PHONY: help

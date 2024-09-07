.DEFAULT_GOAL := help

SHELL := /bin/bash
WORKDIR := .
ENVDIR := $(WORKDIR)/.env

COMPOSE_SERVICE_NAME := "web"

DOCKER_RUN := "docker-compose exec web python"
LOCAL_RUN := "python"

# =============================================================================
# === Detect OS, and set appropriate Environment Variables.
# =============================================================================
ifeq ($(OS), Windows_NT)
	SHELL := /bin/bash
	INIT := python -m venv .env
	ENV := $(ENVDIR)/Scripts
	ACTIVATE := . $(ENV)/activate
	UPIP := $(ENV)/python.exe -m pip install --upgrade pip
else
	SHELL := /bin/bash
	INIT := virtualenv .env
	ENV := $(ENVDIR)/bin
	ACTIVATE := . $(ENV)/activate
	UPIP := $(ENV)/pip install -U  pip

	UNAME_S := $(shell uname -s)
	ifeq ($(UNAME_S), Linux)
		# Do something
	endif
	ifeq ($(UNAME_S), Darwin)
		# Do something
	endif
endif

$(info Detected OS: $(OS))

# =============================================================================
# === Set-up Targets.
# =============================================================================
##@ Set-up
setup: ## Initiate Virtual Environment.
	$(info Initiating Virtual Environment)
	@pip install virtualenv
	$(INIT)
.PHONY: setup

env: setup ## Activate Virtual Environment.
	$(info Activating Virtual Environment)
	$(ACTIVATE)
.PHONY: env

install: env requirements.txt ## Install Requirements.
	$(info Installing Requirements)
	$(UPIP)
	$(ENV)/pip install -Ur requirements.txt --no-cache-dir
.PHONY: install

# =============================================================================
# === Development Targets.
# =============================================================================
##@ Development
test: build ## Run Tests.
	$(info Running Tests)
	@docker-compose -f docker-compose.test.yml run --rm --user $(UID):`id -g` web coverage run --source="." ./manage.py test --settings=settings.testing && coverage report -m --skip-empty && coverage html --skip-empty
.PHONY: test

test-local: install ## Run Tests.
	$(info Running Tests)
	$(ENV)/coverage run --source="." ./src/manage.py test --settings=settings.testing
	$(ENV)/coverage report -m --skip-empty
	$(ENV)/coverage html --skip-empty
.PHONY: test-local

api-test: install ## Run API Tests.
	$(info Running API Tests)
.PHONY: api-test

api-test-local: install ## Run API Tests on local.
	$(info Running API Tests)
.PHONY: api-test-local

int-test: install ## Run Integration Tests.
	$(info Running Integration Tests)
.PHONY: int-test

int-test-local: install ## Run Integration Tests on local.
	$(info Running Integration Tests)
.PHONY: int-test-local

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
.PHONY: swagger-build

swagger-view: ## Run Swagger in the view Mode.
	@cd ./swagger; ./view_or_edit_swagger.sh view
.PHONY: swagger-view

swagger-edit: ## Run Swagger in the edit Mode.
	cd ./swagger; ./view_or_edit_swagger.sh edit
.PHONY: swagger-edit

# =============================================================================
# === CI/CD Targets.
# =============================================================================
##@ CI/CD
login: ## Login the Docker Daemon to AWS ECR.
	$(info Logging the Docker Daemon to AWS ECR.)
.PHONY: login

build: login ## Build the Containers/Images, defined in the `docker-compose`.
	$(info Building the Containers/Images)
	@docker-compose -f docker-compose.yml build --no-cache --pull $(COMPOSE_SERVICE_NAME)
	@docker-compose -f docker-compose.yml --compatibility up --no-start
.PHONY: build

run: build run-int migrate makemessages compilemessages loaddata collectstatic ## Start the `docker-compose`.

run-int: ## Start the Compose.
	$(info Starting the Compose)
	@docker-compose -f docker-compose.yml up -d
.PHONY: run-int

# run-local: prereq-win ## Start the Compose, bypassing Build Steps.
run-local: ## Start the Compose, bypassing Build Steps.
	$(info Starting the Compose)
	@docker-compose -f docker-compose.local.yml up -d
.PHONY: run-local

prereq-win:
	$(info Installing Prerequisits for Windows Platform)
	@choco install make nodejs git
	@npm install -g bower less recess
	@pip install virtualenv
	@python -m venv .env
	$(ACTIVATE_WIN)
	$(ENV_WIN)/pip install -U pip
	$(ENV_WIN)/pip install -Ur requirements.txt --no-cache-dir
.PHONY: prereq-win

prereq-nix:
	$(info Installing Prerequisits for *nix Platform)
.PHONY: prereq-nix

down: ## Clean up the Project Folders.
	$(info Cleaning Things )
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

makemigrations:
	$(info Making Migrations)
	@docker-compose exec web python manage.py makemigrations
.PHONY: makemigrations

migrate:
	$(info Migrating)
	@docker-compose exec web python manage.py migrate
.PHONY: migrate

makemessages:
	$(info Making Messages)
	@docker-compose exec web python manage.py makemessages -l es
	@docker-compose exec web python manage.py makemessages -l de
.PHONY: makemessages

compilemessages:
	$(info Compiling Messages)
	@docker-compose exec web python manage.py compilemessages -l es
	@docker-compose exec web python manage.py compilemessages -l de
.PHONY: compilemessages

loaddata:
	$(info Loading Data)
	@docker-compose exec web python manage.py loaddata admin categories faq faq_sections site teams team_members
.PHONY: loaddata

collectstatic:
	$(info Collecting static Files)
	@docker-compose exec web python manage.py bower install
	@docker-compose exec web python manage.py collectstatic --clear --no-input
.PHONY: collectstatic

# =============================================================================
# === Helpers Targets.
# =============================================================================
##@ Helpers
help: ## Display this Help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
.PHONY: help

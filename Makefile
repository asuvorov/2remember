.DEFAULT_GOAL := help

SHELL := /bin/bash
WORKDIR := .
ENVDIR := $(WORKDIR)/.env
ENV := $(ENVDIR)/bin
ACTIVATE := . $(ENV)/activate

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
##@ Dependencies
deps:  ## Check Dependencies.
	$(info Checking and getting Dependencies)
.PHONY: deps

install: env requirements.txt ## Install Requirements.
	$(info Installing Requirements)
	$(ENV)/pip install -U pip
	$(ENV)/pip install -Ur requirements.txt
.PHONY: install

lint: env ## Run Linter.
	$(info Running Linter)
	$(ENV)/pylint src/ setup.py --reports=y > reports/pylint.report
.PHONY: lint

test: env ## Run Tests.
	$(info Running Tests)
	$(ENV)/coverage run --source="." ./src/manage.py test --settings=settings.testing
	$(ENV)/coverage report
	$(ENV)/coverage html
.PHONY: test

messages: env ## Make and compile Messages.
	$(info Making and compiling Messages)
	$(ENV)/python manage.py makemessages    -l de
	$(ENV)/python manage.py makemessages    -l es
	$(ENV)/python manage.py compilemessages -l de
	$(ENV)/python manage.py compilemessages -l es
.PHONY: messages

##@ Clean-up
clean: ## Clean up the Project Folders.
	$(info Cleaning up Things)
	@rm -rf __pycache__
	@rm -rf *.pyc
	@rm -rf .env
.PHONY: clean

##@ Building
build: clean deps ## Build the Project.
	$(info Building the Project)
.PHONY: build

watch: clean deps ## Watch File Changes and build.
	$(info Watching and building the Project)
.PHONY: watch

##@ Helpers
help: ## Display this Help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
.PHONY: help

# =============================================================================
# Documentation Targets.
# =============================================================================
swagger-build:
	@cd ./swagger; ./view_or_edit_swagger.sh

swagger-view:
	@cd ./swagger; ./view_or_edit_swagger.sh view

swagger-edit:
	@cd ./swagger; ./view_or_edit_swagger.sh edit

# =============================================================================
# ===  CI/CD Targets.
# =============================================================================
tag:
	docker build --target=svc -t $(ECR_REPO):$(TAG) .
	docker build -f Dockerfile_worker --target=worker -t $(ECR_REPO)/worker:$(TAG) .
.PHONY: tag

push:
	docker push "$(ECR_REPO):$(TAG)"
	docker push "$(ECR_REPO)/worker:$(TAG)"
.PHONY: push

.DEFAULT_GOAL := help

ENV_NAME := core
PY_VERSION := "3.12"

# =============================================================================
# === (mini)Conda Targets.
# =============================================================================
##@ Conda
cclean: ## Clean up Conda.
	$(info Cleaning up Conda)
	@conda clean --all -y
.PHONY: cclean

ccreate: ## Create Conda Environment.
	$(info Creating Conda Environment)
	@conda env create --name $(ENV_NAME) -f environment.yml -y
.PHONY: ccreate

cupdate: ## Update Conda Environment.
	$(info Updating Conda Environment)
	@conda env update --file environment.yml --prune
.PHONY: cupdate

cclone: ## Create an identical Environment on the same or another Machine.
	$(info Creating an identical Environment)
	@conda create --name $(ENV_NAME) --file spec-file.txt -y
.PHONY: cclone

cinstall: ## Install listed Packages into an existing Environment.
	$(info Installing Conda Environment Packages)
	@conda install --name $(ENV_NAME) --file spec-file.txt -y
.PHONY: cinstall

cactivate: ## Activate Conda Environment.
	$(info Activating Conda Environment)
	@conda activate $(ENV_NAME)
.PHONY: cactivate

cexport: ## Export Conda Environment.
	$(info Exporting Conda Environment)
	@conda env export --from-history > environment.yml
	@conda list > spec-file.txt
# 	@conda list --explicit > spec-file.txt
.PHONY: cexport

cremove: ## Remove Conda Environment.
	$(info Removing Conda Environment)
	@conda deactivate
	@conda remove --name $(ENV_NAME) --all -y
.PHONY: cremove

cupgrade: ## Upgrade Conda.
	$(info Upgrading Conda)
	@conda conda update --force conda -y
.PHONY: cupgrade

csnippets: ## Run Conda Snippets.
	$(info Running Conda Snippets)
	@conda install conda-forge::pysqlite3 conda-forge::sqlite conda-forge::libsqlite -y
.PHONY: csnippets

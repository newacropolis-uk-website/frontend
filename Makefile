.DEFAULT_GOAL := help
SHELL := /bin/bash

.PHONY: help
help:
	@cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z_-]+:.*?## .*$$' | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: dependencies
dependencies: ## Create the lib for dependencies
	pip install -t lib/ -r requirements.txt

.PHONY: test
test: ## Run all tests
	./scripts/run_tests.sh

.PHONY: run
run: ## Run app - deprecated - use dev-server instead
	./scripts/run_app.sh

.PHONY: dev-server
dev-server: ## Run dev server
	dev_appserver.py app-dev.yaml

.PHONY: tail-logs
tail-logs: ## Tail logs
	gcloud app logs tail -s default   

.PHONY: deploy
deploy: ## Deploy
	gcloud app deploy

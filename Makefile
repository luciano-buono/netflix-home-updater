.PHONY: help sync run lock check-lock check-version lint build-dockerfile docker_login docker_push
.DEFAULT_GOAL := help
.ONESHELL:

# Include sensitive variables to be exported
-include .makerc

help: ## Show available commands
	@awk 'BEGIN {FS = ":.*## "} /^[a-zA-Z_-]+:.*## / {printf "%-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
sync: ## Install locked runtime and development dependencies
	uv sync --locked
run: ## Start the webserver using the uv environment
	uv run --locked python src/app.py
lock: ## Update the dependency lockfile after editing pyproject.toml
	uv lock
check-lock: ## Check that uv.lock matches pyproject.toml
	uv lock --check
check-version:
	@$(if $(strip $(VERSION)),:,$(error VERSION is required. Example: VERSION=2.0 make build-dockerfile))
lint: ## Run pre-commit checks
	uv run --locked pre-commit run --all-files
build-dockerfile: check-version check-lock ## Build the ARM64 Docker image (VERSION required)
	DOCKER_REGISTRY=${DOCKER_REGISTRY} VERSION=${VERSION} docker compose build
docker_login: ## Login to Dockerhub
	docker login -u ${DOCKER_USER} -p "$$(pass ${DOCKER_PASSWORD_PAT})" docker.io
docker_push: check-version ## Push the Docker image (VERSION required)
	docker push ${DOCKER_REGISTRY}:${VERSION}

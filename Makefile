.PHONY: all
.DEFAULT_GOAL := help
.ONESHELL:

# ----------------------------------------------------------------------------
# Local Variables
#
# ============================================================================

DOCKER_REGISTRY=methizul/netflix-home-updater
ENVIRONMENT=development

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "⚡ \033[34m%-30s\033[0m %s\n", $$1, $$2}'

build-requirements:
	# TODO: Right now requirements file is loaded hardcoded in project.toml
	uv pip compile  requirements/${ENVIRONMENT}.in -U --output-file requirements/${ENVIRONMENT}.txt
build:
	pack build ${DOCKER_REGISTRY} --builder paketobuildpacks/builder-jammy-base

docker_login: ## Login to Dockerhub
	docker login -u methizul -p "$$(pass methizul/docker/password)" docker.io

docker_push: ## Pull image from ECR and push to Dockerhub
	docker tag ${DOCKER_REGISTRY}:latest ${DOCKER_REGISTRY}:0.1
	# docker push ${DOCKER_REGISTRY}:$${ECR_TAG}
	docker push ${DOCKER_REGISTRY}:latest

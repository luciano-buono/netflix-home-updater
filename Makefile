.PHONY: all
.DEFAULT_GOAL := help
.ONESHELL:

# ----------------------------------------------------------------------------
# Local Variables
#
# ============================================================================

DOCKER_REGISTRY=methizul/netflix-home-updater
ENVIRONMENT=development
VERSION?=0.1

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "⚡ \033[34m%-30s\033[0m %s\n", $$1, $$2}'

build-pack-requirements:
	# TODO: Right now requirements file is loaded hardcoded in project.toml
	# Paketo does not support ARM, use Heroku buildpack
	# requirements.txt must be in rootdir, cannot be defined with variable
	# https://github.com/heroku/buildpacks/blob/main/docs/python/README.md
	uv pip compile  requirements/${ENVIRONMENT}.in -U --output-file requirements.txt
build-pack:
	# TODO: check if buildpack works now that we use separate container for selenium
	# pack build ${DOCKER_REGISTRY} --builder paketobuildpacks/builder-jammy-base --platform linux/arm64
	pack build ${DOCKER_REGISTRY} --builder heroku/builder:24
build-requirements:
	uv pip compile requirements/${ENVIRONMENT}.in -U --output-file requirements/${ENVIRONMENT}.txt
build-dockerfile:
	DOCKER_REGISTRY=${DOCKER_REGISTRY} ENVIRONMENT=${ENVIRONMENT} docker compose build
docker_login: ## Login to Dockerhub
	docker login -u methizul -p "$$(pass methizul/docker/password)" docker.io

docker_push: ## Pull image from ECR and push to Dockerhub
	docker tag ${DOCKER_REGISTRY}:latest ${DOCKER_REGISTRY}:${VERSION}
	docker push ${DOCKER_REGISTRY}:latest
	docker push ${DOCKER_REGISTRY}:${VERSION}

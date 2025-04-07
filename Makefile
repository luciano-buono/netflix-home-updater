.PHONY: all
.DEFAULT_GOAL := help
.ONESHELL:

# Include sensitive variables to be exported
include .makerc

ENVIRONMENT=development
VERSION?=0.1

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
	docker login -u ${DOCKER_USER} -p "$$(pass ${DOCKER_PASSWORD_PASSCLI})" docker.io
docker_push: ## Pull image from ECR and push to Dockerhub
	docker tag ${DOCKER_REGISTRY}:latest ${DOCKER_REGISTRY}:${VERSION}
	docker push ${DOCKER_REGISTRY}:latest
	docker push ${DOCKER_REGISTRY}:${VERSION}

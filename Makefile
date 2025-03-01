.PHONY: all
.DEFAULT_GOAL := help
.ONESHELL:

# ----------------------------------------------------------------------------
# Local Variables
#
# ============================================================================

DOCKER_REGISTRY=methizul/netflix-home-updater

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "⚡ \033[34m%-30s\033[0m %s\n", $$1, $$2}'

docker_login: ## Login to Dockerhub
	docker login -u methizul -p `pass methizul/docker/password` docker.io

docker_push: ## Pull image from ECR and push to Dockerhub
	docker push ${DOCKER_REGISTRY}:$${ECR_TAG}
	docker push ${DOCKER_REGISTRY}:latest

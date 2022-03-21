.DEFAULT_GOAL := help
PROJECT_NAME = mypydot
DOCKER_IMAGE ?= $(PROJECT_NAME)
LOCAL_ETL_DIR ?= $(shell pwd)

DOCKER_TAG ?= latest

PHONY: build
build:
	@docker build \
		-t $(DOCKER_IMAGE):$(DOCKER_TAG) .


PHONY: run-it
run-it:
	@docker run  -it \
		--name=$(PROJECT_NAME) \
		-v ${LOCAL_ETL_DIR}:/opt/app/ \
		--rm $(DOCKER_IMAGE):$(DOCKER_TAG) bash


PHONY: run-tests
run-tests: build
	@docker run  \
		--name=$(PROJECT_NAME) \
		-v ${LOCAL_ETL_DIR}:/opt/app/ \
		--rm $(DOCKER_IMAGE):$(DOCKER_TAG) poetry run pytest --cov="mypydot" -v tests/ --cov-report=xml --cov-report=html


PHONY: run-lint
run-lint : build
	@docker run  -t \
		--name=$(PROJECT_NAME) \
		--rm $(DOCKER_IMAGE):$(DOCKER_TAG) poetry run flake8

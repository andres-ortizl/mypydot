.DEFAULT_GOAL := help
PROJECT_NAME = mypydot
DOCKER_IMAGE ?= $(PROJECT_NAME)
ENV_FILE ?= .env
LOCAL_ENV_FILE ?= .envrc
LOCAL_ETL_DIR ?= $(shell pwd)

DOCKER_TAG ?= latest

PHONY: build
build:
	@docker build \
		-t $(DOCKER_IMAGE):$(DOCKER_TAG) .

PHONY: run
run:
	@docker run  \
		--name=$(PROJECT_NAME) \
		-v ${LOCAL_ETL_DIR}:/opt/etls/$(PROJECT_NAME) \
		--rm $(DOCKER_IMAGE):$(DOCKER_TAG)

PHONY: run-it
run-it:
	@docker run  -it \
		--name=$(PROJECT_NAME) \
		-v ${LOCAL_ETL_DIR}:/opt/etls/$(PROJECT_NAME) \
		--rm $(DOCKER_IMAGE):$(DOCKER_TAG) bash


PHONY: run-tests
run-tests: build
	@docker run  -t \
		--name=$(PROJECT_NAME) \
		-v ${LOCAL_ETL_DIR}:/opt/etls/$(PROJECT_NAME) \
		--rm $(DOCKER_IMAGE):$(DOCKER_TAG) poetry run pytest

PHONY: run-lint
run-lint : build
	@docker run  -t \
		--name=$(PROJECT_NAME) \
		-v ${LOCAL_ETL_DIR}:/opt/etls/$(PROJECT_NAME) \
		--rm $(DOCKER_IMAGE):$(DOCKER_TAG) poetry run flake8

#-include .env
.EXPORT_ALL_VARIABLES:

# .SILENT:
# Make all targets PHONY, so that you don't need to add .PHONY after every one.
.PHONY: $(MAKECMDGOALS)

AWS_REGION 	?= ap-southeast-2
AWS_PROFILE ?= default
AWS_ACCOUNT ?= 619211191908

IMAGE_NAME ?= colouring-book
IMAGE_TAG  ?= latest
IMAGE_REPO ?= danjw8502
# IMAGE_REPO ?= $(ECR)

GUNICORN_BIND ?= 0.0.0.0:8080
GUNICORN_LOG_LEVEL ?= info

TZ ?= Australia/Brisbane

APP_VERSION := $(IMAGE_TAG)
APP_PORT    ?= 9999

ECR := $(AWS_ACCOUNT).dkr.ecr.$(AWS_REGION).amazonaws.com

build:
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) --build-arg="APP_VERSION=$(IMAGE_TAG)" .

dev:
	gunicorn --config ./gunicorn.conf.py  --log-level debug --reload

run:
	docker compose up

run-dev: build
	docker compose --file compose-dev.yaml up

deploy:
	docker compose up -d

login:
	aws ecr get-login-password --region $(AWS_REGION) --profile $(AWS_PROFILE) | docker login --username AWS --password-stdin $(ECR)

tag: build
	docker tag $(IMAGE_NAME):$(IMAGE_TAG) $(IMAGE_REPO)/$(IMAGE_NAME):$(IMAGE_TAG)
	docker tag $(IMAGE_NAME):$(IMAGE_TAG) $(IMAGE_REPO)/$(IMAGE_NAME):latest

push: tag
	docker push $(IMAGE_REPO)/$(IMAGE_NAME):$(IMAGE_TAG)
	docker push $(IMAGE_REPO)/$(IMAGE_NAME):latest

format:
	black *.py

lint:
	pylint *.py

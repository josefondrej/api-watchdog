IMAGE_NAME?=api-watchdog
IMAGE_TAG?=latest

docker-build:
	docker build -t "$(IMAGE_NAME):$(IMAGE_TAG)" .

docker-run:
	docker run -p 5000:5000 "$(IMAGE_NAME):$(IMAGE_TAG)"
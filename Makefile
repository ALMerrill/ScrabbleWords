NAME	:= amerrill/scrabble-words-backend
TAG	:= $$(git log -1 --pretty=%H)
IMG	:= ${NAME}\:${TAG}
LATEST	:= ${NAME}\:latest
LOCAL_PORT	:= 4200
DOCKER_PORT	:= 80
 
build:
	@docker build -t ${IMG} .
	@docker tag ${IMG} ${LATEST}

run:
	@docker run -p ${LOCAL_PORT}\:${DOCKER_PORT} ${IMG}

push:
	@docker push ${NAME}
#!/bin/sh

gitDir=$(dirname $(realpath $0))
serviceName="customer-manager"

cd ${gitDir}/frontend/docker/Dockerfile
podman build \
    --pull \
    --no-cache \
    --platform=linux/arm64/v8,linux/amd64 \
    -t ${REGISTRY}/$serviceName:frontend \
    ./

podman image push \
    ${REGISTRY}/$serviceName:frontend
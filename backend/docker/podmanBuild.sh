#!/bin/sh

gitDir=$(dirname $(realpath $0))
serviceName="customer-manager"

cd  ${gitDir}/backend/docker/Dockerfile
podman build \
    --pull \
    --no-cache \
    --platform=linux/arm64/v8,linux/amd64 \
    -t ${REGISTRY}/$serviceName:backend \
    ./

podman image push \
    ${REGISTRY}/$serviceName:backend
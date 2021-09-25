#!/bin/sh

gitDir=$(dirname $(realpath $0))
serviceName="customer-manager"

cd ${gitDir}/docker/
podman build \
    --pull \
    --no-cache \
    --platform=linux/arm64/v8,linux/amd64 \
    -t ${REGISTRY}/$serviceName:dev
    ./

podman image push \
    ${REGISTRY}/$serviceName:dev
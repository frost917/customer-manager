#!/bin/bash 
gitDir=$(dirname $(realpath $0))
ver="dev"

#  build
cd  ${gitDir}/

docker buildx build \
    --push \
    --no-cache \
    --platform=linux/amd64 \
    -t ${REGISTRY}/customer-manager:dev \
    ./

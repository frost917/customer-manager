﻿#!/bin/bash 
gitDir=$(dirname $(realpath $0))
ver="dev"

#  build
cd  ${gitDir}/
docker buildx build \
    --push \
    --platform=linux/arm64/v8,linux/amd64 \
    -t ${REGISTRY}/customer-manager:frontend \
    ./Dockerfile.frontend

docker buildx build \
    --push \
    --platform=linux/arm64/v8,linux/amd64 \
    -t ${REGISTRY}/customer-manager:backend \
    ./
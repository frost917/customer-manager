#!/bin/bash 
gitDir=$(dirname $(realpath $0))
ver="dev"

#  build
cd  ${gitDir}/
docker buildx build \
    --push \
    --platform=linux/arm64/v8,linux/amd64 \
    -t ${REGISTRY}/customer-manager:${ver} \
    ./ 

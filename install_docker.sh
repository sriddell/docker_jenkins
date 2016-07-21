#!/bin/bash
set +x
cd /tmp
if ! [ ${CI_DOCKER_VERSION} ]; then
    CI_DOCKER_VERSION=latest
fi
echo "installing docker client binary version $CI_DOCKER_VERSION"
#curl -L https://get.docker.com/builds/Linux/x86_64/docker-$CI_DOCKER_VERSION.tgz -o docker.tgz
curl -L https://get.docker.com/builds/Linux/x86_64/docker-17.04.0-ce.tgz -o docker.tgz
mkdir extract
cd extract
tar xzf ../docker.tgz
if [ -d "docker/completion" ]; then
    rm -rf docker/completion
fi
find -type f -exec mv -i {} /usr/local/bin \;


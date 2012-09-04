#!/bin/bash
echo "Building synapse-client"

cd `dirname $0`
cd ..

git checkout master
git pull

NAME="synapse-client"
VERSION=`git describe --long --match "release*" | awk -F"-" '{print $2}'`
RELEASE=`git describe --long --match "release*" | awk -F"-" '{print $3}'`

./scripts/build-rpm.sh

deploy-trunk /var/lib/mock/epel-6-i386/result/${NAME}-${VERSION}-${RELEASE}.el6.noarch.rpm /public/centos
deploy-trunk /var/lib/mock/fedora-16-i386/result/${NAME}-${VERSION}-${RELEASE}.fc15.noarch.rpm /public/fedora/16
deploy-trunk /var/lib/mock/fedora-17-i386/result/${NAME}-${VERSION}-${RELEASE}.fc16.noarch.rpm /public/fedora/17

updaterepo

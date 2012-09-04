#!/bin/bash

NAME="synapse-client"
platforms=(epel-6-i386 fedora-16-i386 fedora-17-i386)

if [ -z $1 ]
then
  VERSION=`git describe --long --match "release*" | awk -F"-" '{print $2}'`
else
  VERSION=$1
fi

if [ -z $2 ]
then
  RELEASE=`git describe --long --match "release*" | awk -F"-" '{print $3}'`
else
  RELEASE=$2
fi

COMMIT=`git describe --long --match "release*" | awk -F"-" '{print $4}'`

cd `dirname $0`
cd ..

# Generate version file
echo "VERSION=\""$VERSION"\"" > syncli/version.py
echo "RELEASE=\""$RELEASE"\"" >> syncli/version.py

sed "s/#VERSION#/${VERSION}/g" pkg/rpm/${NAME}.spec.template > pkg/rpm/${NAME}.spec
sed -i "s/#RELEASE#/${RELEASE}/g" pkg/rpm/${NAME}.spec
sed -i "s/#COMMIT#/${COMMIT}/g" pkg/rpm/${NAME}.spec

tar -cvzf $HOME/rpmbuild/SOURCES/${NAME}-${VERSION}-${RELEASE}.tar.gz * \
--exclude-vcs \
--exclude build \
--exclude dist \
--exclude tests \
--exclude "*.egg-info" \
--exclude pkg

rpmbuild -ba pkg/rpm/${NAME}.spec

for platform in "${platforms[@]}"
do
    /usr/bin/mock -r ${platform} --rebuild $HOME/rpmbuild/SRPMS/${NAME}-${VERSION}-${RELEASE}*.src.rpm
done

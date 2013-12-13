#!/bin/sh
set -x -e
version="2.2.5"
rm -rf BUILD RPMS SRPMS tmp || true
mkdir -p BUILD RPMS SRPMS SOURCES
spectool -g -A fixmystreet.spec -d "version $version" -C SOURCES
rpmbuild -bb --define="_topdir $PWD" --define="_tmppath $PWD/tmp" --define="version $version" fixmystreet.spec

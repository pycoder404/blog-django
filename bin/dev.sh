#!/usr/bin/env bash
#  active the virtual python env
set -ex
export DJANGO_DEBUG=1
export DJANGO_MEDIA=1

BIN_DIR=$(cd `dirname $0`; pwd)
BASE_DIR=`dirname ${BIN_DIR}`
echo -e "BASE_DIR is: ${BASE_DIR}"

cd ${BASE_DIR}
python manage.py runserver 0:28088

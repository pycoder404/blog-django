#!/usr/bin/env bash
set -ex
export DJANGO_DEBUG=
export DJANGO_MEDIA=

BIN_DIR=$(cd `dirname $0`; pwd)
BASE_DIR=`dirname ${BIN_DIR}`
echo -e "BASE_DIR is: ${BASE_DIR}"
mkdir -p /var/log/uwsgi/
mkdir -p /var/run/
cd ${BASE_DIR}
# uwsgi --socket :8001 --module Secbackend.wsgi  --buffer-size 65536 --chmod-socket=666

uwsgi --chdir=${BASE_DIR} \
    --module=Myblog.wsgi:application \
    --env DJANGO_SETTINGS_MODULE=Myblog.settings \
    --master --pidfile=/var/run/uwsgi.pid \
    --socket=127.0.0.1:8001 \
    --processes=5 \
    --uid=1000 --gid=2000 \
    --harakiri=20 \
    --max-requests=5000 \
    --vacuum \
    --daemonize=/var/log/uwsgi/django_8001.log
#     --home=/path/to/virtual/env \   # optional path to a virtual environment
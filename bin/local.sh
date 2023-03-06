#!/usr/bin/env bash
set -ex
export DJANGO_DEBUG=
export DJANGO_ENV="local"

BIN_DIR=$(cd `dirname $0`; pwd)
BASE_DIR=`dirname ${BIN_DIR}`
echo -e "BASE_DIR is: ${BASE_DIR}"
mkdir -p /var/log/uwsgi/
mkdir -p /var/run/
cd ${BASE_DIR}
# uwsgi --socket :8001 --module Secbackend.wsgi  --buffer-size 65536 --chmod-socket=666


# 如果需要调测的话，在生产环境可以配合设置DJANGO_DEBUG=1，并注释下面的--daemonize行
uwsgi --chdir=${BASE_DIR} \
    --module=MyBlog.wsgi:application \
    --env DJANGO_SETTINGS_MODULE=MyBlog.settings \
    --master --pidfile=/var/run/uwsgi.pid \
    --socket=127.0.0.1:8001 \
    --buffer-size 65536 \
    --processes=5 \
    --harakiri=20 \
    --buffer-size 65536 \
    --max-requests=5000 \
    --vacuum \
    --daemonize=/var/log/uwsgi/django_8001.log
#     --home=/path/to/virtual/env \   # optional path to a virtual environment
#    --uid=1000 --gid=2000 \

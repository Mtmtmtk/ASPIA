#!/bin/bash

rm -rf .pid/
envsubst '$$REDIS_ADDRESS' < ${BACKEND_HOME}/config_server.ini.template > ${BACKEND_HOME}/config_server.ini
python -m ducts server start &

if [ "$1" = "dev" ]; then
    watchmedo shell-command -W -R -p '*.py' -c 'echo ${watch_src_path}; python -m ducts server stop && python -m ducts server start' ./
else
    /bin/bash
fi


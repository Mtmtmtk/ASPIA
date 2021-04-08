#!/bin/bash

rm -rf ./.pid
envsubst '$$REDIS_ADDRESS' < ${BACKEND_HOME}/config_server.ini.template > ${BACKEND_HOME}/config_server.ini
python -m ducts server start &
watchmedo shell-command -W -R -p '*.py' --ignore-patterns="projects/*/*" -c 'echo ${watch_src_path}; python -m ducts server stop && python -m ducts server start' ./

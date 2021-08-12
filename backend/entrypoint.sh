#!/bin/bash

rm -rf .pid/
envsubst '$$REDIS_ADDRESS' < $HOME/config/config_server.ini.template > $HOME/config/config_server.ini
python -m ducts server start -c ./config/config_server.ini &

if [ "$SERVICE_NAME" = "backend-dev" ]; then
    watchmedo shell-command -W -R -p '*.py' -c 'echo ${watch_src_path}; python -m ducts server stop && python -m ducts server start -c ./config/config_server.ini' ./
else
    /bin/bash
fi


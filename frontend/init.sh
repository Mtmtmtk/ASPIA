#!/bin/ash

npm install

if [ "$1" = "dev" ]; then
    npm run serve
else
    npm run build
fi

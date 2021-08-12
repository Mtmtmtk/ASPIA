#!/bin/ash

if [ "$SERVICE_NAME" = "frontend-dev" ]; then
    npm run serve
else
    npm run build
fi

#!/bin/ash

if [ "$1" = "prodonly" ]; then
    RUN envsubst '$$PORT $$DOMAIN_NAME $$BACKEND_ADDRESS' < /etc/nginx/nginx.conf.template.prodonly > /etc/nginx/nginx.conf
else
    RUN envsubst '$$PORT $$DEV_PORT $$DOMAIN_NAME $$DEV_DOMAIN_NAME $$FRONTEND_DEV_ADDRESS $$BACKEND_ADDRESS $$BACKEND_DEV_ADDRESS' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf
fi

nginx

if [ $ENABLE_SSL = 1 ] ; then
    certbot --nginx -d ${DOMAIN_NAME} -m ${EMAIL} --agree-tos -n
    certbot renew
    nginx -s reload
fi

/bin/ash

#!/bin/ash

chmod +rx /var/www/html/dist

if [ "$1" = "prodonly" ]; then
    envsubst '$$HTTP_PORT $$DOMAIN_NAME $$BACKEND_ADDRESS' < /etc/nginx/nginx.conf.template.prodonly > /etc/nginx/nginx.conf
else
    envsubst '$$HTTP_PORT $$DEV_HTTP_PORT $$DOMAIN_NAME $$DEV_DOMAIN_NAME $$DEV_FRONTEND_ADDRESS $$BACKEND_ADDRESS $$DEV_BACKEND_ADDRESS' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf
fi

nginx

if [ $ENABLE_SSL -eq 1 ] ; then
    certbot --nginx -d ${DOMAIN_NAME} -m ${EMAIL} --agree-tos -n
    certbot renew
    nginx -s reload
fi

if [ $DEV_ENABLE_SSL -eq 1 ] ; then
    certbot --nginx -d ${DEV_DOMAIN_NAME} -m ${DEV_EMAIL} --agree-tos -n
    certbot renew
    nginx -s reload
fi

/bin/ash

FROM nginx:alpine

RUN apk update && apk --update --no-cache add wget curl python3 certbot certbot-nginx

COPY ./init.sh /init.sh
COPY ./nginx.conf.template /etc/nginx/nginx.conf.template

ENTRYPOINT ["/init.sh"]

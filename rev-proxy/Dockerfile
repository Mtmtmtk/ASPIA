FROM nginx:alpine

#RUN apk update && apk --update --no-cache add wget curl python2 certbot certbot-nginx

COPY ./nginx.conf.template /etc/nginx/nginx.conf.template
ARG DOMAIN_NAME
RUN envsubst '$$DOMAIN_NAME' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

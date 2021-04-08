FROM nginx:alpine

#RUN apk update && apk --update --no-cache add wget curl python2 certbot certbot-nginx

ARG DOMAIN_NAME
ARG DEV_DOMAIN_NAME
ARG FRONTEND_DEV_ADDRESS
ARG BACKEND_ADDRESS
ARG BACKEND_DEV_ADDRESS

COPY ./nginx.conf.template /etc/nginx/nginx.conf.template

RUN envsubst '$$DOMAIN_NAME $$DEV_DOMAIN_NAME $$FRONTEND_DEV_ADDRESS $$BACKEND_ADDRESS $$BACKEND_DEV_ADDRESS' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

#CMD ["/bin/ash"]

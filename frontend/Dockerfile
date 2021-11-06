FROM node:lts-alpine3.12

ARG HOME
WORKDIR $HOME

ARG SERVICE_NAME
ENV SERVICE_NAME ${SERVICE_NAME}

RUN apk add git python3 make g++

COPY ./package.json .
RUN npm install

COPY ./ ./

ENTRYPOINT ["./entrypoint.sh"]

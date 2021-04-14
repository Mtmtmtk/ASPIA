FROM node:lts-alpine3.12

ARG HOME
WORKDIR $HOME

RUN apk add git

COPY package.json* ./

ENTRYPOINT ["./init.sh"]

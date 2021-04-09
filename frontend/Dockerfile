FROM node:lts-alpine3.12

ARG HOME
WORKDIR $HOME

RUN apk add git

COPY package.json* ./
RUN npm install

COPY ./ .

CMD ["npm","run","build"]

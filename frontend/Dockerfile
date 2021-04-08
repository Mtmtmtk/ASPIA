FROM node:lts-alpine3.12

ARG FRONTEND_HOME
WORKDIR $FRONTEND_HOME

RUN apk add git

COPY package.json* ./
RUN npm install

RUN npm install @iflb/ducts

CMD ["npm","run","serve"]

# docker-compose-vue-ducts
"Vanilla" Docker Compose environment for Vue CLI frontend and DUCTS backend

## What it does

- Allows you to instantly prototype applications with [Vue CLI](https://cli.vuejs.org/) frontend and [DUCTS](https://github.com/iflb/ducts) backend
- Reverse-proxying i) frontend server, ii) backend server, iii) [Redis](https://redis.io/) database, and iv) static files, with [Nginx](https://www.nginx.com/)
- Launches dev. environment (for both frontend/backend) that can be accessed from any URL domain / port number, as specified in configuration
- Quick SSL adaptation with [Let's Encrypt](https://letsencrypt.org/)

## Structure

```
.
├── _yml/
│   ├── docker-compose.yml                  # common docker compose schema
│   ├── docker-compose.prod.yml             # schema for production environment
│   ├── docker-compose.dev.yml              #            dev. environment
│   └── docker-compose.redis.dev.yml        #            dev. redis container
├── rev-proxy/
│   ├── Dockerfile                          # docker image scheme for prod+dev server
│   ├── Dockerfile-prodonly                 #                         prod server only
│   ├── nginx.conf.template                 # nginx.conf for prod+dev server (env vars are substituted w/ envsubst)
│   ├── nginx.conf.template.prodonly        #                prod server only
│   └── init.sh                             # docker container entrypoint
├── frontend/
│   ├── Dockerfile                          # docker image scheme for prod server
│   ├── Dockerfile-dev                      #                         dev server
│   └── (Vue CLI-relevant dirs/files)
├── backend/
│   ├── Dockerfile                          # docker image scheme for prod server
│   ├── Dockerfile-dev                      #                         dev server
│   ├── config_server.ini.template          # DUCTS' config file (env vars are substituted w/ envsubst)
│   ├── init.sh                             # docker container entrypoint
│   └── (DUCTS-relevant dirs/files)
├── redis/
│   ├── data/                               # dump file location for prod redis
│   └── data-dev/                           #                        dev redis
├── static/
│   └── (blank)                             # location for serving static files
└── .env                                    # environment variables for project configuration
```

## Build & Run

0. Install [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)

1. Clone this repository

2. Open `.env` and edit as needed.

The two main user scenarios are:

i. **(For public domain deployment)** Production server: https://yourdomain.com/ ; Development server: http://dev.yourdomain.com/

ii. **(For localhost development)** Production server: http://localhost/ ; Development server: http://localhost:8080/


Example for the scenario (i):

```diff
...

- ENABLE_SSL=0
- EMAIL=
+ ENABLE_SSL=1
+ EMAIL=for.letsencrypt.registration@yourdomain.com

# =========

- DOMAIN_NAME=localhost
+ DOMAIN_NAME=yourdomain.com

...

# =========

- DEV_DOMAIN_NAME=localhost
- DEV_PORT=8080
+ DEV_DOMAIN_NAME=test.yourdomain.com
+ DEV_PORT=80

...
```

3. Build.

```
sudo docker-compose build
```

4. Run.

```
sudo docker-compose up
```

## Preview

Say your production server is at https://yourdomain.com/ and development server at http://dev.yourdomain.com/ :

- Vue frontend project can be accessed at: https://yourdomain.com/

- DUCTS' Web Service Descriptor access point is at: https://yourdomain.com/ducts/wsd

- Static files at `./static/img/my_img.jpg` can be found at: https://yourdomain.com/static/img/my_img.jpg

- Redis database (prod) is at: yourdomain.com:6379 (by default, or whatever specified in `.env`)

- Redis database (dev) is at: yourdomain.com:6380 (by default, or whatever specified in `.env`)

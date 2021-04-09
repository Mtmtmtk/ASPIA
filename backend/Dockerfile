FROM python:3.9-slim-buster

ARG HOME

WORKDIR $HOME

RUN apt-get update && \
    apt-get install -y gcc gettext-base && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install ducts watchdog pyyaml argh

COPY init.sh ./init.sh
RUN chmod +x ./init.sh

ENTRYPOINT ["./init.sh"]

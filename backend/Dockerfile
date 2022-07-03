FROM python:3.9-slim-buster

ARG HOME
WORKDIR $HOME

ARG SERVICE_NAME
ENV SERVICE_NAME ${SERVICE_NAME}

RUN apt-get update && \
    apt-get install -y gcc gettext-base && \
    apt-get install -y libsndfile1-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY ./pyproject.toml .

RUN pip install -U pip && pip install poetry 

RUN poetry config virtualenvs.create false
RUN poetry install

RUN pip install scipy && pip install resampy

COPY ./ .

ENTRYPOINT ["./entrypoint.sh"]

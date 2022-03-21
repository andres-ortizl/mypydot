FROM python:3.9-slim

LABEL maintainer="andrs.ortizl@gmail.com" \
      app="mypydot" \
      stack="python"

RUN apt-get update && apt-get install -y --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir --upgrade "poetry==1.1.11"

ARG BASE_ROUTE=/opt/app/
ENV PYTHONPATH=/opt/app/
WORKDIR "${BASE_ROUTE}"

COPY poetry.lock "${BASE_ROUTE}"
COPY pyproject.toml "${BASE_ROUTE}"

# hadolint ignore=SC2046
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

COPY . ${BASE_ROUTE}
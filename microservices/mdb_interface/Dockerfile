ARG PYTHON_TAG=python:3.10-slim-bullseye

FROM ${PYTHON_TAG} AS builder

# Note: venv is created in pndo-python-base

ENV PATH="/app/venv/bin:$PATH"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY pyproject.toml .

COPY src /app/src
RUN pip install ./

#
# Publishing Image
#

FROM ${PYTHON_TAG} AS publisher

RUN groupadd -g 999 python && \
    useradd -r -u 999 -g python python

RUN mkdir /app && chown python:python /app

COPY --chown=python:python --from=builder /vault /vault
COPY --chown=python:python --from=builder /usr/bin/jq /usr/bin/
COPY --chown=python:python --from=builder /app/runtime_libs /usr/lib

COPY --chown=python:python --from=builder /app/venv /app/venv

COPY --chown=python:python --chmod=755 docker/entrypoint.sh /app/
COPY --chown=python:python --chmod=644 docker/healthcheck.py /app/

USER 999

WORKDIR /app

# Run our app in the virtual environment

ENV PATH="/app/venv/bin:$PATH"

CMD ["python", "-m", "app"]

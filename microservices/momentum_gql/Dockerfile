ARG PYTHON_TAG=python:3.10-slim-bullseye

FROM ${PYTHON_TAG}

# Note: venv is created in pndo-python-base

ENV PATH="/app/venv/bin:$PATH"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY pyproject.toml .

COPY src /app/src
RUN pip install ./

WORKDIR /app

# Run our app in the virtual environment

ENV PATH="/app/venv/bin:$PATH"

CMD ["python", "-m", "app"]

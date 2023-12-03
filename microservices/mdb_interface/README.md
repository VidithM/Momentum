# GraphQL App

## Local development

Create a virtual environment and install the project in
dev mode by using the venv target in the Makefile.

```bash
make venv
source .venv/bin/activate
```

## Run

### Setup Environment

```bash
source .venv/bin/activate
make requirements
pip install -e ".[dev]"
pip install -r requirements

```

### Run the application

While in the top level directory (and in virtual environment)

`python -m app --port=8020`

### Run the Sequel Server

```bash
docker compose up
```

The commands for creating the tables are under the python create_table funciton in the database folder.

### API

Get or Post requests to _____

Otherwise, post to localhost:8020 a proper gql request.

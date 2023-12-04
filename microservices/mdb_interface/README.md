# GraphQL App

## Local development

Create a virtual environment

```bash
python3 -m venv .venv
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

`python -m app --port=8011`

### API

Get or Post requests to _____

Otherwise, post to localhost:8011 per the restful api described in Main.  test_api.py automates this, use this to test.

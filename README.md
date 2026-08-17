# contabo_s3_tutorial
This tutorial walks readers through interacting with Contabo's S3 compatible object storage using a Python backend. It allows for uploading media files, viewing them, and deleting them all from a single API.

## Pre-requisites
- [Python](https://python.org) 3.14.0+
- [UV package manager](https://docs.astral.sh/uv/getting-started/installation/)
- [Make](https://askappsec.com/book/chapter-1/installing-make/)(optional)

## Setup & Installation
#### Option 1: Using Make
- Run `make env_setup` and populate env file
- Run `make local_setup` to install dependencies and run project

#### Option 2: Using UV
- Create and populate `.env` file
- Run `uv sync` to install dependencies
- Run project using `uv run --env-file .env main.py`

## API Docs

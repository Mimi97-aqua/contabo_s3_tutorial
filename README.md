# contabo_s3_tutorial
This tutorial walks readers through interacting with Contabo's S3 compatible object storage using a Python backend. It allows for uploading media files, viewing them, and deleting them all from a single API.

You can read the medium article using this link: 

## Pre-requisites
- [Python](https://python.org) 3.14.0+
- [UV package manager](https://docs.astral.sh/uv/getting-started/installation/)
- [Make](https://askappsec.com/book/chapter-1/installing-make/)(optional)
- [Docker](https://docs.docker.com/desktop/)(optional)

## Setup & Installation
#### Option 1: Using Make
- Run `make env_setup` and populate env file
- Run `make local_setup` to install dependencies and run project

#### Option 2: Using UV
- Create and populate `.env` file
- Run `uv sync` to install dependencies
- Run project using `uv run --env-file .env main.py`

#### Option 3: Using Docker

## API Docs
Base URL: `localhost:5000/api`
#### 1. Generate Upload URL `POST /`
- Generates the URL which the frontend uses for making the upload.
- This endpoint allows for only uploads of media files (images, videos, and audios) not more than 5MB.
- When testing on an API client like Postman, your request should have `multipart/form-data` as its body with the parameter of the uploaded file being exactly the string `file`

#### 2. Performing the actual upload `PUT /<upload_url>`
- Since there is no frontend app to consume this, testing will still be done with an API client to mimic the frontend behaviour.
- Create a new PUT request and paste the upload URL from the previous request in the URL bar.
- For the headers, specify `Content-Type` to be the value of the content type from the previous request.
- In the body, select `application/octet-stream` (binary) and upload the same file you uploaded when making the previous request.
- Your file will be successfully uploaded to Contabo. **PS:** uploading a file with the same name replaces the existing file on the object storage.

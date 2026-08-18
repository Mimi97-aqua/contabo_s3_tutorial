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
- Base URL: `http://localhost:5000/api`
- **Note:** All presigned URLs generated expire after 1 hour

#### 1. Generate Upload URL: `POST /`
- Generates the presigned URL which the frontend uses for making the upload.
- This endpoint allows for only uploads of media files (images, videos, and audios) not more than 5MB.
- When testing on an API client like Postman, your request should have `multipart/form-data` as its body with the parameter of the uploaded file being exactly the string `file`

#### 2. Performing the actual upload: `PUT /<upload_url>`
- Since there is no frontend app to consume this, testing will still be done with an API client to mimic the frontend behaviour.
- Create a new PUT request and paste the upload URL from the previous request in the URL bar.
- For the headers, specify `Content-Type` to be the value of the content type from the previous request.
- In the body, select `application/octet-stream` (binary) and upload the same file you uploaded when making the previous request.
- Your file will be successfully uploaded to Contabo. **PS:** uploading a file with the same name replaces the existing file on the object storage.

#### 3. View File: `GET /`
- Requires `file_url` and `content_type` as JSON payload. They were both returned in the response of generating the upload URL.
- Checks if file exists by fetching its metadata headers and throws an error if it doesn't
- Generates presigned URL used for viewing/downloading the content.
- Paste the generated URL in your browser to view/download the content.

#### 4. Deleting File: `DELETE /`
- Requires `file_url` as JSON payload.
- Checks if file exists by fetching its metadata headers and throws an error if it doesn't
- Generates preseigned URL for deleting and rather than sending the URL to the client to hit for deleting, the backend does the deleting directly my making a DELETE request to the generated URL. This is because unlike uploading (which can hog server RAM) and viewing (which can contain private files) which send the presigned URL to the client, deleting is a tiny command (in which no file transfer is happening).
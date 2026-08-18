FROM python:3.14
LABEL description="Contabo S3 interaction with Python Backend"
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY . .
RUN uv sync
EXPOSE 5000
CMD ["uv", "run", "main.py"]

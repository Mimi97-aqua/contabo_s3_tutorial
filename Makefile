.PHONY: env_setup local_setup

env_setup:
	@echo "1: Setting up environment variables..."
	@touch .env
	@echo ".env file created. Please fill in the required environment variables."

local_setup:
	@echo "2: Setting up local environment..."
	@uv sync
	@echo "Installing dependencies..."
	@echo "3: Running the application..."
	@uv run --env-file .env main.py
	
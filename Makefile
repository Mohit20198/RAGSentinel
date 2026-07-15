# Makefile for RAGSentinel

.PHONY: install install-dev format lint typecheck test run-backend run-ui clean docker-up docker-down

# Install dependencies
install:
	pip install -r requirements.txt

# Format code using Ruff
format:
	ruff check --select I --fix .
	ruff format .

# Lint code using Ruff
lint:
	ruff check .

# Static type checking using mypy
typecheck:
	mypy app/

# Run unit tests
test:
	pytest tests/ -v

# Run the FastAPI backend locally
run-backend:
	uvicorn app.main:app --reload --port 8000

# Run the Streamlit UI locally
run-ui:
	streamlit run ui/app.py

# Clean up cache directories
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

# Start the application using Docker Compose
docker-up:
	docker-compose up --build

# Stop the Docker Compose application
docker-down:
	docker-compose down

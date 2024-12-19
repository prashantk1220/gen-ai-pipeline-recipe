# Use the official Python image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install system dependencies for psycopg2 and Pillow
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy project files to the container
COPY pyproject.toml poetry.lock ./
COPY data ./data/
COPY whats_for_dinner/ ./whats_for_dinner/

# Configure Poetry to install dependencies
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

# Expose the port FastAPI runs on
EXPOSE 8080

# Set the default command
CMD ["poetry", "run", "start"]

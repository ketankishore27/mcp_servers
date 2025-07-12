# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install uv globally
RUN pip install --no-cache-dir uv

# Copy dependency files first for caching
COPY pyproject.toml ./
COPY uv.lock ./

# Install dependencies using uv sync
RUN uv sync

# Copy the rest of the project files
COPY server.py ./

# Expose port (change if your server uses a different port)
EXPOSE 8000

# Run the server
CMD ["uv", "run", "server.py"]

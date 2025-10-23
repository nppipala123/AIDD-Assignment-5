# Multi-stage Dockerfile for a small Flask app

# Builder stage (installs dependencies)
FROM python:3.11-slim AS builder
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /install

# Install build deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN python -m pip install --upgrade pip
RUN python -m pip install --prefix=/install -r requirements.txt --no-cache-dir

# Final stage (runtime)
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY . /app

# Create a non-root user
RUN groupadd -r app && useradd -r -g app app
RUN chown -R app:app /app
USER app

EXPOSE 5000

CMD ["python", "app.py"]

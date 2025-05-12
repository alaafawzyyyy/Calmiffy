# Stage 1: Install dependencies
FROM python:3.9-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PORT=8000

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libffi-dev libssl-dev curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy only requirements first to leverage cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final image
FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

# Copy installed packages from previous stage
COPY --from=base /usr/local/lib/python3.9 /usr/local/lib/python3.9
COPY --from=base /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

# Clean up __pycache__ and unnecessary files
RUN find . -type d -name "__pycache__" -exec rm -r {} + || true

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Use an official Python runtime as a parent image
FROM python:3.9-slim AS build

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PORT=8000

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements to leverage Docker cache
COPY requirements.txt .

# Install dependencies in a single step and clean up cache
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

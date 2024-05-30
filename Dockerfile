# Use an official Python runtime as the base image
FROM python:3.9-slim-buster

# Set environment variables to ensure proper build behavior
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create and change to the app directory, keeping it separate from the base image
WORKDIR /app

# Copy only the requirements.txt file to leverage Docker caching
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev musl-dev && \
    pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Run database migrations
RUN python manage.py migrate

# Expose the port that the application will run on
EXPOSE 8000

# Set the default command to run when the container starts
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--config", "gunicorn-cfg.py", "core.wsgi"]

# Add a healthcheck to ensure the container is running as expected
HEALTHCHECK --interval=10s --timeout=3s --retries=3 CMD [ "curl", "--fail", "http://localhost:8000/healthz" ] || exit 1

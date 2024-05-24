FROM python:3.9-slim-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# change to /app directory
WORKDIR /app

# copy requirements.txt and install dependencies
COPY requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev musl-dev && \
    pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# copy the rest of the code
COPY . .

# run migrations
RUN python manage.py migrate

# expose the port
EXPOSE 8000

# run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--config", "gunicorn-cfg.py", "core.wsgi"]

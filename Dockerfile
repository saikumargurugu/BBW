# Use official Python base image
FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /code

# Install dependencies
COPY requirements.txt .
RUN apt-get update && apt-get install -y postgresql-client && \
    pip install --no-cache-dir -r requirements.txt && \
    python -m pip install firebase-admin && \
    python -m pip install Pillow && \
    python -m pip install django-redis  # Install django-redis for Redis integration

# Copy project files
COPY . .

# Expose port
EXPOSE 8000

# Run server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Use official Python base image
FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1


# Set working directory
WORKDIR /code

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE 8000

# Run server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

#!/bin/bash

# Step 1: Generate SSL Certificate (Self-Signed)
echo "Generating self-signed SSL certificates..."

mkdir -p nginx/certs

openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/certs/localhost.key \
  -out nginx/certs/localhost.crt \
  -subj "/CN=localhost"

echo "SSL certificates generated at nginx/certs/"

# Step 2: Update nginx.conf with SSL Configuration
echo "Updating nginx.conf with SSL support..."

cat > nginx/nginx.conf <<EOL
events {}

http {
    server {
        listen 80;
        listen 8000;

        location / {
            proxy_pass http://web:8000;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }

        location /static/ {
            alias /code/static/;
        }

        location /media/ {
            alias /code/media/;
        }
    }

    server {
        listen 443 ssl;

        ssl_certificate /etc/nginx/certs/localhost.crt;
        ssl_certificate_key /etc/nginx/certs/localhost.key;

        location / {
            proxy_pass http://web:8000;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }

        location /static/ {
            alias /code/static/;
        }
    }
}
EOL

echo "nginx.conf updated."

# Step 3: Print instructions to modify docker-compose.yml

echo "Please ensure your docker-compose.yml is configured to mount the SSL certificates and nginx.conf."

echo "Example configuration for your nginx service in docker-compose.yml:

  nginx:
    image: nginx:latest
    ports:
      - \"80:80\"
      - \"8000:8000\"
      - \"443:443\"
    depends_on:
      - web
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/certs:/etc/nginx/certs
      - .:/code
"

echo "Once you've updated your docker-compose.yml, run the following commands to start the services."

echo "docker-compose down"
echo "docker-compose up --build"

echo "Setup complete. Follow the instructions to start your containers."

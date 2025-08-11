# Dockerfile for Web-based VPS Service
FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    docker.io \
    nginx \
    python3 \
    python3-pip \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install Docker Compose
RUN curl -L "https://github.com/docker/compose/releases/download/v2.20.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

# Set up the web interface
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .

# Set up Python requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Configure nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Set up basic auth
RUN apt-get update && apt-get install -y apache2-utils
RUN htpasswd -b -c /etc/nginx/.htpasswd $BASIC_AUTH_USERNAME $BASIC_AUTH_PASSWORD

# Expose ports
EXPOSE 80
EXPOSE 2375

# Start services
CMD service docker start && \
    nginx && \
    python3 /app/api/server.py & \
    node /app/server.js

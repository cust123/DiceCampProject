#!/bin/bash

# Stop existing containers
docker-compose down

# Pull the latest images
docker pull $DOCKER_USERNAME/client-app:latest
docker pull $DOCKER_USERNAME/server-app:latest

# Start updated containers
docker-compose up -d
# Wait for the services to be ready
echo "Waiting for services to start..."
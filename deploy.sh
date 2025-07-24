#!/bin/bash
set -euo pipefail

# Ensure DOCKER_USERNAME is set
if [ -z "${DOCKER_USERNAME:-}" ]; then
  echo "❌ ERROR: DOCKER_USERNAME is not set!"
  exit 1
fi

echo "✅ Using Docker Hub username: $DOCKER_USERNAME"

echo "🔻 Stopping existing containers..."
docker-compose down

echo "⬇️ Pulling latest images from Docker Hub..."
docker pull "${DOCKER_USERNAME}/client-app:latest"
docker pull "${DOCKER_USERNAME}/server-app:latest"

echo "🚀 Starting up with new images..."
docker-compose up -d

echo "⏳ Waiting for services to settle..."
sleep 10

echo "✅ Deploy complete."

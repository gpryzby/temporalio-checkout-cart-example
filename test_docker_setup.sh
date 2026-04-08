#!/bin/bash

echo "Testing Docker setup for Temporalio checkout cart example"

# Build the Docker images
echo "Building Docker images..."
docker-compose build

# Start the services
echo "Starting Temporal server and worker..."
docker-compose up -d

# Wait a moment for services to start
sleep 5

# Check if services are running
echo "Checking running containers..."
docker-compose ps

# Run a test workflow
echo "Running test workflow..."
docker-compose run --rm starter

# Stop the services
echo "Stopping services..."
docker-compose down

echo "Docker setup test completed!"
#!/bin/sh

# Start the services with Docker Compose
docker-compose up -d redis
docker-compose up -d web
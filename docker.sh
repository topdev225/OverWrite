#!/bin/bash
docker-compose -f docker-compose-prod.yaml down
docker-compose -f docker-compose-prod.yaml build
docker-compose -f docker-compose-prod.yaml up -d
echo "Waiting 20s for containers to come online..."
sleep 20
docker-compose -f docker-compose-prod.yaml ps
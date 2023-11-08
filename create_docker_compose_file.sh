#!/bin/bash

# Ensure jq is installed
if ! command -v jq &> /dev/null
then
    echo "jq could not be found. Please install it to proceed."
    exit 1
fi

# The JSON file containing the service configurations
JSON_FILE="docker-services.json"

# Header for the docker-compose file
DISCLAIMER="# This file is generated automatically by generate-compose.sh. Do not edit manually.\n"

# The template for the docker-compose services
read -r -d '' COMPOSE_TEMPLATE << EOM
version: '3.7'
services:
EOM

# Append the services from the JSON file to the docker-compose template
while IFS= read -r SERVICE_NAME; do
  # Extract values from JSON using jq
  HOSTNAME=$(jq -r --arg SERVICE_NAME "$SERVICE_NAME" '.services[] | select(.service_name==$SERVICE_NAME) | .hostname' "$JSON_FILE")
  CONTAINER_NAME=$(jq -r --arg SERVICE_NAME "$SERVICE_NAME" '.services[] | select(.service_name==$SERVICE_NAME) | .container_name' "$JSON_FILE")
  CONFIG_PATH=$(jq -r --arg SERVICE_NAME "$SERVICE_NAME" '.services[] | select(.service_name==$SERVICE_NAME) | .config_path' "$JSON_FILE")

  # Append each service to the COMPOSE_TEMPLATE
  COMPOSE_TEMPLATE+="
  $CONTAINER_NAME:
    build: ./mqttPub
    container_name: $CONTAINER_NAME
    hostname: $HOSTNAME
    volumes:
      - $CONFIG_PATH:/app/data/conf.json
    networks:
      - mqtt_network
    logging:
      options:
        max-size: '10m'
        max-file: '3'
"
done < <(jq -r '.services[].service_name' "$JSON_FILE")

# Append network configuration to the COMPOSE_TEMPLATE
COMPOSE_TEMPLATE+="
networks:
  mqtt_network:
    driver: bridge
"

# Save the template to docker-compose_generated.yml
echo -e "$DISCLAIMER$COMPOSE_TEMPLATE" > docker-compose_generated.yml

echo "docker-compose_generated.yml file has been created successfully."
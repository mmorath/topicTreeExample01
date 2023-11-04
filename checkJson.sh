#!/bin/bash

# Define the directory containing JSON files.
JSON_DIR="./mqttPub/data"

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "jq could not be found, please install it to run this script."
    exit 1
fi

# Loop through each JSON file in the directory and check its validity.
for json_file in "$JSON_DIR"/*.json; do
    echo "Checking $json_file..."
    if jq empty "$json_file" > /dev/null 2>&1; then
        echo "Valid JSON file: $json_file"
    else
        echo "Invalid JSON file: $json_file"
        # Uncomment the line below if you want the script to exit on the first error
        # exit 1
    fi
done

echo "JSON validation check completed."

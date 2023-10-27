#!/bin/bash

# Clear the screen
clear

# Script start time
START_TIME=$(date +%s)

# Print the script start time and user
echo "Script started at: $(date)"
echo "User: $(whoami)"

# Delete -e files in the current directory and its subdirectories
find . -type f -name "*-e" -exec rm {} +

# Script end time
END_TIME=$(date +%s)

# Calculate time taken
TIME_TAKEN=$((END_TIME - START_TIME))

# Summary
echo "Script executed by: $(whoami)"
echo "Script started at: $(date -d @$START_TIME)"
echo "Script ended at: $(date -d @$END_TIME)"
echo "Time taken: $TIME_TAKEN seconds"

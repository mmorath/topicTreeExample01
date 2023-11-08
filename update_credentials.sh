#!/bin/bash

# Clear the screen
clear

# Script start time
START_TIME=$(date +%s)

# Print the script start time and user
echo "Script started at: $(date)"
echo "User: $(whoami)"

# Store the current directory
START_DIR=$(pwd)

# Initialize count variable to track total email replacements
COUNT=0

# Email to be replaced
OLD_EMAIL="old-email@example.com"
# New email
NEW_EMAIL="new-email@example.com"

# Debug information
echo "Searching for email: $OLD_EMAIL"
echo "Replacement email: $NEW_EMAIL"

# Temp file to hold lines where email is found
TEMP_FILE=$(mktemp)

# Search for files containing the old email and note down the line numbers
find "$START_DIR" -type f -exec grep -n -H "$OLD_EMAIL" {} + > $TEMP_FILE

# Show files and line numbers where old email is found
while IFS= read -r line; do
  COUNT=$((COUNT + 1))
  echo "$line"
done < "$TEMP_FILE"

# Display total emails to be replaced
echo "Total email addresses to be replaced: $COUNT"

# Confirm from user
read -p "Do you want to replace all these occurrences? (y/n): " answer

if [ "$answer" == "y" ]; then
  while IFS= read -r line; do
    file=$(echo $line | cut -d: -f1)
    if [[ "$OSTYPE" == "darwin"* ]]; then
      # macOS
      sed -i "" "s/$OLD_EMAIL/$NEW_EMAIL/g" "$file"
    else
      # Linux
      sed -i "s/$OLD_EMAIL/$NEW_EMAIL/g" "$file"
    fi
  done < "$TEMP_FILE"
  echo "Replaced all occurrences."
else
  echo "No replacements made."
fi

# Remove the temporary file
rm "$TEMP_FILE"

# Script end time
END_TIME=$(date +%s)

# Calculate time taken
TIME_TAKEN=$((END_TIME - START_TIME))

# Summary
echo "Script executed by: $(whoami)"
echo "Script started at: $(date -d @$START_TIME)"
echo "Script ended at: $(date -d @$END_TIME)"
echo "Time taken: $TIME_TAKEN seconds"
echo "Old email: $OLD_EMAIL"
echo "New email: $NEW_EMAIL"

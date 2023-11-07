#!/bin/bash

# Function to generate a random password that meets the specified criteria
generate_password() {
    local password_length=9
    while :; do
        # Generate a random password
        password=$(tr -dc 'A-Za-z0-9' < /dev/urandom | fold -w ${password_length} | head -n 1)
        # Check if the password meets the requirements for digits and uppercase letters
        if [[ $password =~ [A-Z] ]] && [[ $password =~ [0-9] ]]; then
            echo "$password"
            break
        fi
    done
}

# Function to create or backup the .env file
create_env_file() {
    local env_file="users.env"
    if [[ -f "$env_file" ]]; then
        # Backup the existing file
        mv "$env_file" "${env_file}_backup_$(date +%F_%T)"
    fi
    touch "$env_file"
}

# Main script execution
main() {
    # Prepare the .env file
    create_env_file

    # Predefined users
    usernames=("airpressure" "cooling" "exhaust" "fit" "gas" "iiot_box" "mde" "mes" "power" "scanner")

    # Generate and assign new passwords for each user
    for username in "${usernames[@]}"; do
        password=$(generate_password)
        echo "user=\"$username\"; password=\"$password\"" >> users.env
    done

    echo "Generated new passwords for each user and saved to users.env"
}

# Run the main function
main

#!/bin/bash

# Global Settings
OE_CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
OE_CURRENT_USER=$(whoami)

# Functions
check_root_permissions() {
    if [ "$EUID" -ne 0 ]; then
        echo "These operations require administrative privileges. Please run them with sudo."
        exit 1
    fi
}

update_linux() {
    apt-get update -y
    apt-get full-upgrade -y
}

install_linux_dependencies() {
    apt-get install libatlas-base-dev -y
    apt-get install python3-venv -y
}

install_mac_dependencies() {
    if ! command -v brew &>/dev/null; then
        echo "Homebrew not found. Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    else
        echo "Homebrew is already installed. Skipping..."
    fi
    brew update
    brew upgrade
    brew install python3
}

create_venv() {
    if [ ! -d "$OE_CURRENT_DIR/venv" ]; then
        python3 -m venv $OE_CURRENT_DIR/venv
    fi
}

install_python_packages() {
    source $OE_CURRENT_DIR/venv/bin/activate
    pip install wheel
    pip install -r requirements.txt
}

# Main Script
clear
echo "### OE_CURRENT_DIR=$OE_CURRENT_DIR"
echo "### OE_CURRENT_USER=$OE_CURRENT_USER"

# Detect OS
if [ "$(uname)" == "Darwin" ]; then
    os_name="macOS"
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    os_name="Linux"
fi
echo "#### Detected operating system: $os_name"

# Conditional Operations
if [ "$os_name" == "Linux" ]; then
    check_root_permissions
    update_linux
    install_linux_dependencies
elif [ "$os_name" == "macOS" ]; then
    install_mac_dependencies
fi

# Common Operations
create_venv
install_python_packages

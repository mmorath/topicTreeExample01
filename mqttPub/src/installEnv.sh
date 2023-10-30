#!/bin/bash
clear
echo -e "############################################################################"
echo -e "##### Script for preparing the environment                                 #"
echo -e "##### author: Matthias Morath 2020-10-03 kompass_eng_0x@icloud.com         #"
echo -e "##### tested on:                                                           #"
echo -e "#####  -Ubuntu 20.04.01                                                    #"
echo -e "############################################################################"

# Global Settings
OE_CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Function to get the current user
get_current_user() {
    if [ "$(uname)" == "Darwin" ]; then
        echo $USER
    elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
        echo $USER
    fi
}

OE_CURRENT_USER=$(get_current_user)
echo -e "### OE_CURRENT_DIR=$OE_CURRENT_DIR"
echo -e "### OE_CURRENT_USER=$OE_CURRENT_USER"
echo -e "############################################################################"

# Detect Operating System
if [ "$(uname)" == "Darwin" ]; then
    os_name="macOS"
    os_version=$(sw_vers -productVersion)
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    os_name="Linux"
    os_version=$(lsb_release -rs)
fi
echo -e "#### Detected operating system: $os_name $os_version"
echo -e "############################################################################"

# For operations that need administrative privileges
if [ "$os_name" == "Linux" ]; then
    echo -e "#### Check if running with administrative privileges"
    echo -e "############################################################################"
    if [ "$EUID" -ne 0 ]; then
        echo -e "These operations require administrative privileges. Please run them with sudo."
        exit 1
    fi
    echo -e "############################################################################"
    echo -e "#### update, upgrade, install python3 and pip3                             #"
    echo -e "############################################################################"
    apt-get update -y
    apt-get full-upgrade -y
    apt-get install libatlas-base-dev -y
    apt-get install python3-venv -y
fi

# macOS package management
if [ "$os_name" == "macOS" ]; then
    if ! command -v brew &>/dev/null; then
        echo "Homebrew not found. Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    else
        echo "Homebrew is already installed. Skipping..."
    fi
    brew update
    brew upgrade
    brew install python3
fi

# Check for virtual environment and create if it doesn't exist
echo -e "############################################################################"
echo -e "#### Check if virtual environment exists"
echo -e "############################################################################"
if [ ! -d "$OE_CURRENT_DIR/venv" ]; then
    echo -e "############################################################################"
    echo -e "#### virtual env does not exist, create a virtual environment"
    echo -e "############################################################################"
    python3 -m venv $OE_CURRENT_DIR/venv
fi

# Activate virtual environment
echo -e "############################################################################"
echo -e "#### activate the virtual environment"
echo -e "############################################################################"
source $OE_CURRENT_DIR/venv/bin/activate
which python
python3 --version
which pip
pip3 --version

# Install the requirements
echo -e "############################################################################"
echo -e "#### install the requirements"
echo -e "############################################################################"
pip install wheel
pip install -r requirements.txt

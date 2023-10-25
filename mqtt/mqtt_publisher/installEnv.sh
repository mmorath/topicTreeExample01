#!/bin/bash                                                             
clear                                                                           
echo -e "############################################################################"
echo -e "##### Script for preparing the enviroment                                  #"
echo -e "##### author: Matthias Morath 2020-10-03 matthias.morath@liebherr.com      #"
echo -e "##### tested on:                                                           #"
echo -e "#####  -Ubuntu 20.04.01                                                    #"
echo -e "############################################################################"
echo -e "### global settings #"
OE_CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
OE_FOLDER="folder"
OE_CONFIG="config.txt"

echo -e "### OE_CURRENT_DIR=$OE_CURRENT_DIR"
echo -e "### OE_FOLDER=$OE_FOLDER"
echo -e "### OE_CONFIG=$OE_CONFIG"
echo -e "### OE_CURRENT_USER=$OE_CURRENT_USER"

echo -e "############################################################################"
echo -e "#### install git, vim and set vim as global git core.editor                #"
echo -e "############################################################################"
echo -e "#### install git.."
sudo apt install -y git
echo -e "#### install vim that you can commit with git using vim "
sudo apt install -y vim
echo -e "#### setting up vim as default editor of choice "
git config --global core.editor "vim"
export GIT_EDITOR=vim
# typical modeline useful for python vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 --> ~/.vimrc
echo -e "############################################################################"
echo -e "#### update, upgrade, install python3 and pip3                             #"
echo -e "############################################################################"
sudo apt-get update -y
sudo apt-get full-upgrade -y
sudo apt-get install libatlas-base-dev -y
sudo apt-get install python3-venv -y
echo -e "############################################################################"
echo -e "#### Check if virtual environment exist "
echo -e "############################################################################"
if [ ! -d "/$OE_CURRENT_DIR/venv" ];
then
    echo -e "############################################################################"
    echo -e "#### virtual env does not exist, create a virtual environment"
    echo -e "############################################################################"
    python3 -m venv $OE_CURRENT_DIR/venv
fi
echo -e "############################################################################"
echo -e "#### activate the virtual environment"
echo -e "############################################################################"
source $OE_CURRENT_DIR/venv/bin/activate
which python
python3 --version
which pip
pip3 --version
echo -e "############################################################################"
echo -e "#### install the requirements"
echo -e "############################################################################"
pip install wheel
pip install -r requirements.txt

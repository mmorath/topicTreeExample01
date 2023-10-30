#!/bin/bash
clear
echo -e "############################################################################"
echo -e "##### Script for stopping all running Docker containers                   #"
echo -e "##### author: Matthias Morath 2020-10-03 kompass_eng_0x@icloud.com      #"
echo -e "##### tested on:                                                           #"
echo -e "#####  -Ubuntu 20.04.01                                                    #"
echo -e "############################################################################"
# Stop all running containers
docker stop $(docker ps -q)

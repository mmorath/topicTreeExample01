#!/bin/bash
clear                                                                           
echo -e "############################################################################"
echo -e "##### Script for deleting all docker & docker-compose related              #"
echo -e "#####    - volumes                                                         #"
echo -e "#####    - networks                                                        #"
echo -e "#####    - images                                                          #"
echo -e "##### author: Matthias Morath 2020-10-03 kompass_eng_0x@icloud.com      #"
echo -e "##### tested on:                                                           #"
echo -e "#####  -Ubuntu 20.04.01                                                    #"
echo -e "############################################################################"
echo -e "### global settings #"
docker system prune --force --all
#docker stop $(docker ps -a -q)
#docker ps 
docker volume prune  
docker network prune 
docker image prune 

#docker system prune -a

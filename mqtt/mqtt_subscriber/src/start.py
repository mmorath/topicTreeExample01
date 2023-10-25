#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# =============================================================================
__author__ = "Matthias Morath"
__copyright__ = "Copyright 2021"
__credits__ = ["Matthias Morath"]
__license__ = "GPL"
__version__ = "3.0"
__maintainer__ = "Matthias Morath"
__email__ = "matthias.morath@liebherr.com"
__status__ = "Development"
# =============================================================================

import paho.mqtt.client as mqttPubSub
import signal
import sys
import time
import socket
import json
import os
import logging
import logging.config

from datetime import datetime
from time import sleep
from random import randrange

MICROSERVICE_NAME = None
MICROSERVICE_VERSION = None
NTP_HOST_01 = None
NTP_HOST_02 = None
MQTT_HOST = None
MQTT_PORT = None
MQTT_ENABLE_SSL = None
MQTT_USER = None
MQTT_PASSWORD = None
SUBSCRIBER_NAME = None
SUBSCRIBER_DESCRIPTION = None
LOGGING_LEVEL = None

#dictionary of eviroment variables inlcuding type
envVariables = {
        'MICROSERVICE_NAME':"%s",
        'MICROSERVICE_VERSION':"%s",
        'MQTT_HOST':"%s",
        'MQTT_PORT':"%i",
        'MQTT_ENABLE_SSL':"%s",
        'MQTT_USER':"%s",
        'MQTT_PASSWORD':"%s",
        'SUBSCRIBER_NAME':"%s",
        'SUBSCRIBER_DESCRIPTION':"%s",
        'LOGGING_LEVEL': "%s",
}

###############################################################################################################
# logging setup
###############################################################################################################

# set up the logger based on the logger.conf file.
logging.config.fileConfig(fname='./data/logger.conf', disable_existing_loggers=False)

# Get the logger specified in the file
logger = logging.getLogger(__name__)

#Logging Level Mapping
logger_level_mapping = {
    "NOTSET": logging.NOTSET,
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}

###############################################################################################################
# Envrioment settings helper function
###############################################################################################################
def importEnviromentVariables(envDict):
    """ import enviroment variables ...enviroment variables are set in docker-compose file """
    logging.info('Reading enviroment variables from host')
    #create a list which will hold missing env variables
    missingEnvVars = []
    #for each item in the envDict dictionary
    for item in envDict:
        #read the envrioment variable from operating system
        val = os.environ.get(item)
        #Check if read input is type none or has no entry
        if (val == None) or (val == ""):
            #if value is missing append it to the list
            missingEnvVars.append(item)
        else:
            #check for type string
            if (envDict[item] == "%s"):
                exec(("%s = "+envDict[item]) % (item, val),globals())
            #check for type int    
            elif(envDict[item] == "%i"):
                exec(("%s = "+envDict[item]) % (item, int(val)),globals())
            #check for type boolean
            elif(envDict[item] == "%r"):
                exec(("%s = "+envDict[item]) % (item, json.loads(val.lower())),globals())
            else:
                #unknown type not defined...
                logging.debug(f"Unknown type")
    #if list holds missing variables
    if len(missingEnvVars) > 0:
        #return false and the list of missing variables
        return False, missingEnvVars
    else:
        #return true with emtpy list
        return True, []

def setLoggingLevel():
    global logging, logger, logger_level_mapping
    logging.getLogger().setLevel(logger_level_mapping[LOGGING_LEVEL])

###############################################################################################################
# Helper functions host
###############################################################################################################
def get_microServiceInfo():
    """ get all enviroment infos"""
    logging.info('Micro Service started')
    logging.info(f"CONTAINER_NAME: {socket.gethostname()} CONTAINER_IP: {socket.gethostbyname(socket.gethostname())}")
    logging.info('Service startet with the following enviroment variables')
    logging.info(f"MICROSERVICE_NAME:{MICROSERVICE_NAME} MICROSERVICE_VERSION:{MICROSERVICE_VERSION}")
    logging.info(f"SUBSCRIBER_NAME:{SUBSCRIBER_NAME} SUBSCRIBER_DESCRIPTION:{SUBSCRIBER_NAME}")
    logging.info(f"LOGGING_LEVEL:{LOGGING_LEVEL}")
    logging.info(f"MQTT_HOST:{MQTT_HOST} MQTT_PORT:{MQTT_PORT}")
    logging.info(f"MQTT_ENABLE_SSL:{MQTT_ENABLE_SSL} MQTT_USER:{MQTT_USER} MQTT_PASSWORD:{MQTT_PASSWORD}")

def handle_interrupt(client, signal, frame):
    """ Disconnect the client gracefully """
    client.disconnect()
    client.loop_stop()
    logging.info('MQTT client disconnected')
    sys.exit(0)

def subscribe_topics_from_json(client,json_file):
    """ Read topics from JSON file and subscribe to the topic"""
    try:
        with open(json_file, 'r') as file:
            topics = json.load(file)
            logging.info(f"JSON file '{json_file}' could be read an parsed")

            # Subscribe to each topic in the JSON file
            for item in topics:
                topic = item["topic"]
                qos = item["qos"]
                client.subscribe(topic, qos=qos)
                logging.info(f"Subscribed to topic: {topic} with QoS: {qos}")
  
    except FileNotFoundError:
        logging.info(f"JSON file '{json_file}' not found.")
        return
    except json.JSONDecodeError as e:
        logging.info(f"Error parsing JSON file '{json_file}': {str(e)}")
        return    
###############################################################################################################
# MQTT callbacks
###############################################################################################################
def on_connect(client, userdata, flags, rc, properties=None):
    """ callback on connect """
    global flag_connected
    if rc == 0:     
        flag_connected = True
        logging.info('Connected successfully to mqtt host: %s on port: %s',MQTT_HOST,MQTT_PORT)
    else:
        flag_connected = False
        logging.info('No connection to mqtt host: %s on port: %s, returned result code: %s',MQTT_HOST,MQTT_PORT,str(rc))
     
def on_disconnect(client, userdata, rc):
    """ callback on disconnect """
    logging.debug('Disconnected to mqtt host: %s on port %s with result code %s',MQTT_HOST,MQTT_PORT,str(rc))
    client.loop_stop()   

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    """ callback on subscribe """
    logging.debug("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    """ callback on message for when a PUBLISH message is received from the server """
    payload = str(msg.payload.decode("utf-8"))
    logging.debug('Recieve topic: %s payload: %s qos: %s retain: %s',msg.topic,payload,msg.qos,msg.retain)

def on_log(client, userdata, level, buf):
    """ callback for logging """
    logging.debug('%s',buf)

###############################################################################################################
# MAIN
###############################################################################################################
if __name__ == "__main__":
    #import the variables
    importEnviromentVariables(envVariables)
    #set logging level
    setLoggingLevel()
    #provide information about the micro service and its set enviroment variables...
    #note the envrioment variables are set in the docker-compose file
    get_microServiceInfo()
    #create flag_connected which shows if connected or not
    flag_connected = False
    # using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
    # userdata is user defined data of any type, updated by user_data_set()
    # client_id is the given name of the client
    client = mqttPubSub.Client(client_id=MICROSERVICE_NAME, userdata=None, protocol=mqttPubSub.MQTTv5)
    # attach callbacks 
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.on_log = on_log
    client.on_subscribe = on_subscribe
    # Register the interrupt handler
    signal.signal(signal.SIGINT, handle_interrupt)

    if MQTT_ENABLE_SSL:
        # enable TLS
        client.tls_set(tls_version=mqttPubSub.ssl.PROTOCOL_TLS)
        #set username and password
        client.username_pw_set(MQTT_USER,MQTT_PASSWORD)
    try:
        # connect to MQTT broker on port
        client.connect(MQTT_HOST,MQTT_PORT)
        # Subscribe to all topics of encyclopedia by using the wildcard "#"
        #client.subscribe("emt/#", qos=1)
        subscribe_topics_from_json(client,'./data/topics.json')
        # Start the MQTT client loop (runs forever)
        client.loop_forever()
    except KeyboardInterrupt:
        handle_interrupt(None, None)

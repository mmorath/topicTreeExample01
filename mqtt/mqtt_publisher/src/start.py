#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# =============================================================================
__author__ = "Matthias Morath"
__copyright__ = "Copyright 2021"
__credits__ = ["Matthias Morath"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Matthias Morath"
__email__ = "kompass_eng_0x@icloud.com"
__status__ = "Development"
# =============================================================================

import paho.mqtt.client as mqttPubSub
import time
import socket
import json
import os
import logging
import logging.config

from datetime import datetime
from time import sleep
from random import randrange, randint

MICROSERVICE_NAME = None
MICROSERVICE_VERSION = None
NTP_HOST_01 = None
NTP_HOST_02 = None
MQTT_HOST = None
MQTT_PORT = None
MQTT_ENABLE_SSL = None
MQTT_USER = None
MQTT_PASSWORD = None
PUPLISHER_NAME = None
PUPLISHER_DESCRIPTION = None
DIVISION = None
SITE = None
BUILDING = None
DEPARTMENT = None
MACHINE = None
UPDATE_RATE = None
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
        'DIVISION':"%s",
        'SITE':"%s",
        'BUILDING':"%s",
        'DEPARTMENT':"%s",
        'MACHINE':"%s",
        'PUPLISHER_NAME':"%s",
        'UPDATE_RATE': "%i",
        'LOGGING_LEVEL': "%s",
}

# set default update rate
UPDATE_RATE = 1000

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

def setUpdateRate():
    global UPDATE_RATE
    UPDATE_RATE = UPDATE_RATE / 1000
###############################################################################################################
# Helper functions host
###############################################################################################################
def get_microServiceInfo():
    """ get all enviroment infos"""
    logging.info('Micro Service started')
    logging.info(f"CONTAINER_NAME: {socket.gethostname()} CONTAINER_IP: {socket.gethostbyname(socket.gethostname())}")
    logging.info('Service startet with the following enviroment variables')
    logging.info(f"MICROSERVICE_NAME:{MICROSERVICE_NAME} MICROSERVICE_VERSION:{MICROSERVICE_VERSION}")
    logging.info(f"DIVISION:{DIVISION} SITE:{SITE} BUILDING:{BUILDING}")
    logging.info(f"DEPARTMENT:{DEPARTMENT} MACHINE:{MACHINE}")
    logging.info(f"PUPLISHER_NAME:{PUPLISHER_NAME} ")
    logging.info(f"LOGGING_LEVEL:{LOGGING_LEVEL} UPDATE_RATE:{UPDATE_RATE}")
    logging.info(f"MQTT_HOST:{MQTT_HOST} MQTT_PORT:{MQTT_PORT}")
    logging.info(f"MQTT_ENABLE_SSL:{MQTT_ENABLE_SSL} MQTT_USER:{MQTT_USER} MQTT_PASSWORD:{MQTT_PASSWORD}")
###############################################################################################################
# MQTT callbacks
###############################################################################################################
def on_connect(client, userdata, flags, rc):
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
    logging.info('Disconnected to mqtt host: %s on port %s with result code %s',MQTT_HOST,MQTT_PORT,str(rc))
    client.loop_stop()   

def on_message(client, userdata, msg):
    """ callback on message for when a PUBLISH message is received from the server """
    payload = str(msg.payload.decode("utf-8"))
    logging.debug('Recieve topic: %s payload: %s qos: %s retain: %s',msg.topic,payload,msg.qos,msg.retain)

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    """ callback on publish """
    logging.debug("mid: " + str(mid))

def on_log(client, userdata, level, buf):
    """ callback for logging """
    logging.debug('%s',buf)

#def buildTopic(parameter):
#    """ callback for logging """ 
#    return f"{DIVISION}/{SITE}/{BUILDING}/{DEPARTMENT}/{MACHINE}/{PUPLISHER_NAME}/{parameter}".lower()

def buildTopic(category,parameter):
    """ callback for logging """ 
    return f"{DIVISION}/{SITE}/{BUILDING}/{DEPARTMENT}/{MACHINE}/{PUPLISHER_NAME}/{category}/{parameter}".lower()    

def buildTopicPayload(variable,value,unit):
    """ callback for logging """
    tmpdictionary = {
                    'timestamp': time.time(),
                    'timestampreadable': datetime.now().strftime("%d-%m-%Y_%H:%M:%S.%f")[:-3],
                    'variable':variable,
                    'value':value,
                    'unit':unit
                    }
    return json.dumps(tmpdictionary).lower()

###############################################################################################################
# MAIN
###############################################################################################################
if __name__ == "__main__":
    #import the variables
    importEnviromentVariables(envVariables)
    #set logging level
    setLoggingLevel()
    #set update rate
    setUpdateRate()
    #provide information about the micro service and its set enviroment variables...
    #note the envrioment variables are set in the docker-compose file
    get_microServiceInfo()
    #create flag_connected which shows if connected or not
    flag_connected = False
    # create the client
    client = mqttPubSub.Client(MICROSERVICE_NAME)
    # attach callbacks 
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.on_log = on_log
    client.on_publish =on_publish

    if MQTT_ENABLE_SSL:
        # enable TLS
        client.tls_set(tls_version=mqttPubSub.ssl.PROTOCOL_TLS)
        #set username and password
        client.username_pw_set(MQTT_USER,MQTT_PASSWORD)

    # connect to MQTT broker on port
    try:
        client.connect(MQTT_HOST,MQTT_PORT)
    except:
        pass 

    #start the loop
    client.loop_start()  

   #Wait for connection
    while flag_connected != True:
        #sleep for x seconds
        sleep(UPDATE_RATE)
        try:
            #connection is open
            while True:
                if True:
                    #loop through the register
                    ###############################################################################################################
                    # Add here your registers for publishing them to mqtt
                    ###############################################################################################################
                    logging.debug('publish data')
                    #iiot_box_alive#
                    client.publish(buildTopic("iiot_box_alive","xHeartbeat"), buildTopicPayload(variable="xHeartbeat", value = randint(0,1), unit ="boolean"))
                    #iiot_box_ouputs#
                    client.publish(buildTopic("iiot_box_ouputs","xPushButtonIndicatorB"),buildTopicPayload(variable="xPushButtonIndicatorB", value = randint(0,1), unit ="boolean"))  
                    client.publish(buildTopic("iiot_box_ouputs","xPushButtonIndicatorG"),buildTopicPayload(variable="xPushButtonIndicatorG", value = randint(0,1), unit ="boolean"))                   
                    client.publish(buildTopic("iiot_box_ouputs","xPushButtonIndicatorR"),buildTopicPayload(variable="xPushButtonIndicatorR", value = randint(0,1), unit ="boolean"))  
                    client.publish(buildTopic("iiot_box_ouputs","xSignalLampBuzzer"),buildTopicPayload(variable="xSignalLampBuzzer", value = randint(0,1), unit ="boolean"))  
                    client.publish(buildTopic("iiot_box_ouputs","xSignalLampSegment01"),buildTopicPayload(variable="xSignalLampSegment01", value = randint(0,1), unit ="boolean"))  
                    client.publish(buildTopic("iiot_box_ouputs","xSignalLampSegment02"),buildTopicPayload(variable="xSignalLampSegment02", value = randint(0,1), unit ="boolean"))  
                    client.publish(buildTopic("iiot_box_ouputs","xSignalLampSegment03"),buildTopicPayload(variable="xSignalLampSegment03", value = randint(0,1), unit ="boolean"))  
                    client.publish(buildTopic("iiot_box_ouputs","xSignalLampSegment04"),buildTopicPayload(variable="xSignalLampSegment04", value = randint(0,1), unit ="boolean"))  
                    #iiot_box_inputs#
                    client.publish(buildTopic("iiot_box_inputs","xDoorSwitch"),buildTopicPayload(variable="xDoorSwitch", value = randint(0,1), unit ="boolean"))  
                    client.publish(buildTopic("iiot_box_inputs","xEmergencyStop"),buildTopicPayload(variable="xEmergencyStop", value = randint(0,1), unit ="boolean"))  
                    client.publish(buildTopic("iiot_box_inputs","xKeyLockPos1"),buildTopicPayload(variable="xKeyLockPos1", value = randint(0,1), unit ="boolean"))  
                    client.publish(buildTopic("iiot_box_inputs","xKeyLockPos2"),buildTopicPayload(variable="xKeyLockPos2", value = randint(0,1), unit ="boolean"))  
                    client.publish(buildTopic("iiot_box_inputs","xPowerSupply24VOK"),buildTopicPayload(variable="xPowerSupply24VOK", value = randint(0,1), unit ="boolean"))  
                    client.publish(buildTopic("iiot_box_inputs","xPowerSupply48VOK"),buildTopicPayload(variable="xPowerSupply48VOK", value = randint(0,1), unit ="boolean"))  
                    client.publish(buildTopic("iiot_box_inputs","xServiceButton"),buildTopicPayload(variable="xServiceButton", value = randint(0,1), unit ="boolean"))              
                    client.publish(buildTopic("iiot_box_inputs","xVoltagePresent"),buildTopicPayload(variable="xVoltagePresent", value = randint(0,1), unit ="boolean"))              
                    #mde_signals#
                    client.publish(buildTopic("mde_signals","xAutomaticSwitchOff"),buildTopicPayload(variable="xAutomaticSwitchOff", value = randint(0,1), unit ="boolean"))
                    client.publish(buildTopic("mde_signals","xMainCircuitSwitchOn"),buildTopicPayload(variable="xMainCircuitSwitchOn", value = randint(0,1), unit ="boolean"))  
                    client.publish(buildTopic("mde_signals","xProgramStop"),buildTopicPayload(variable="xProgramStop", value = randint(0,1), unit ="boolean"))  
                    client.publish(buildTopic("mde_signals","xLaserActive"),buildTopicPayload(variable="xLaserActive", value = randint(0,1), unit ="boolean"))  
                    client.publish(buildTopic("mde_signals","xImpulse"),buildTopicPayload(variable="xImpulse", value = randint(0,1), unit ="boolean"))  
                    client.publish(buildTopic("mde_signals","xSumError"),buildTopicPayload(variable="xSumError", value = randint(0,1), unit ="boolean"))  
                    client.publish(buildTopic("mde_signals","xProductionTime"),buildTopicPayload(variable="xProductionTime", value = randint(0,1), unit ="boolean"))  
                    client.publish(buildTopic("mde_signals","xTargetCountReached"),buildTopicPayload(variable="xTargetCountReached", value = randint(0,1), unit ="boolean"))  
                    #plc_stats#
                    client.publish(buildTopic("plc_stats","sActualHostName"),buildTopicPayload(variable="pfc200-test", value = randint(0,1), unit ="string" ))
                    client.publish(buildTopic("plc_stats","sDateLocal"),buildTopicPayload(variable="sDateLocal", value = randint(0,1), unit ="string"))  
                    client.publish(buildTopic("plc_stats","sDisplayMode"),buildTopicPayload(variable="sDisplayMode", value = randint(0,1), unit ="string"))  
                    client.publish(buildTopic("plc_stats","sDomainName"),buildTopicPayload(variable="sDomainName", value = randint(0,1), unit ="string"))  
                    client.publish(buildTopic("plc_stats","sFirmwareRevision"),buildTopicPayload(variable="sFirmwareRevision", value = randint(0,1), unit ="string"))  
                    client.publish(buildTopic("plc_stats","sHostName"),buildTopicPayload(variable="sHostName", value = randint(0,1), unit ="string"))  
                    client.publish(buildTopic("plc_stats","sIpAddress_X1"),buildTopicPayload(variable="sIpAddress_X1", value = randint(0,1), unit ="string"))  
                    client.publish(buildTopic("plc_stats","sIpAddress_X2"),buildTopicPayload(variable="sIpAddress_X2", value = randint(0,1), unit ="string"))  
                    client.publish(buildTopic("plc_stats","sLicenseInformation"),buildTopicPayload(variable="sLicenseInformation", value = randint(0,1), unit ="string"))
                    client.publish(buildTopic("plc_stats","sMacAddress_X1"),buildTopicPayload(variable="sMacAddress_X1", value = randint(0,1), unit ="string"))  
                    client.publish(buildTopic("plc_stats","sMacAddress_X2"),buildTopicPayload(variable="sMacAddress_X2", value = randint(0,1), unit ="string"))  
                    client.publish(buildTopic("plc_stats","sOrderNumber"),buildTopicPayload(variable="sOrderNumber", value = randint(0,1), unit ="string"))  
                    client.publish(buildTopic("plc_stats","sProductDescription"),buildTopicPayload(variable="sProductDescription", value = randint(0,1), unit ="string"))  
                    client.publish(buildTopic("plc_stats","sSubNetMask_X1"),buildTopicPayload(variable="sSubNetMask_X1", value = randint(0,1), unit ="string"))  
                    client.publish(buildTopic("plc_stats","sSubNetMask_X2"),buildTopicPayload(variable="sSubNetMask_X2", value = randint(0,1), unit ="string"))  
                    client.publish(buildTopic("plc_stats","sTimeLocal"),buildTopicPayload(variable="sTimeLocal", value = randint(0,1), unit ="string"))  
                    client.publish(buildTopic("plc_stats","sTimeUtc"),buildTopicPayload(variable="sTimeUtc", value = randint(0,1), unit ="string"))  
                    client.publish(buildTopic("plc_stats","xEnable_X1"),buildTopicPayload(variable="xEnable_X1", value = randint(0,1), unit ="string"))  
                    client.publish(buildTopic("plc_stats","xEnable_X2"),buildTopicPayload(variable="xEnable_X2", value = randint(0,1), unit ="string"))  
                    sleep(UPDATE_RATE)
                else:
                    #connection is not open
                    #try to open it again
                    sleep(1)
        #break loop if keyboard interrupt...        
        except KeyboardInterrupt:
            #disconnect the client
            client.disconnect()
            #stop the client loop
            client.loop_stop()     

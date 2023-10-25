#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# =============================================================================
__author__ = "Matthias Morath"
__copyright__ = "Copyright 2021"
__credits__ = ["Matthias Morath"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Matthias Morath"
__email__ = "matthias.morath@gmail.com"
__status__ = "Development"
# =============================================================================
import time
import sys
from barcodeReader import barcode_reader
from readLogConfig import configure_logging_from_file
from mqttClient import MQTTClient 
from readConfig import read_configuration

def main():
    logger = configure_logging_from_file()
    # Read the configuration from config.json
    config_file_path = '/app/data/config.json'  # Update with your config file path
    config_data = read_configuration(config_file_path)
    # if the configuration file cannot be read...else quit
    if config_data is None:
        logger.error("Failed to read configuration. Exiting...")
        sys.exit("Error: Failed to read the configuration. Program terminated.")

    # Set the parameters
    MQTT_HOST = config_data.get("MQTT_HOST", {}).get("value")
    MQTT_PORT = config_data.get("MQTT_PORT", {}).get("value")
    MQTT_ENABLE_SSL = config_data.get("MQTT_ENABLE_SSL", {}).get("value")
    MQTT_USER = config_data.get("MQTT_USER", {}).get("value")
    MQTT_PASSWORD = config_data.get("MQTT_PASSWORD", {}).get("value")
    SUBSCRIBER_NAME = config_data.get("SUBSCRIBER_NAME", {}).get("value")
    SUBSCRIBER_DESCRIPTION = config_data.get("SUBSCRIBER_DESCRIPTION", {}).get("value")
    DIVISION = config_data.get("DIVISION", {}).get("value")
    SITE = config_data.get("SITE", {}).get("value")
    BUILDING = config_data.get("BUILDING", {}).get("value")
    DEPARTMENT = config_data.get("DEPARTMENT", {}).get("value")
    MACHINE = config_data.get("MACHINE", {}).get("value")
    DEVICE = config_data.get("DEVICE", {}).get("value")
    # Create the topic with the specified structure
    TOPIC = f"{DIVISION}/{SITE}/{BUILDING}/{DEPARTMENT}/{MACHINE}/{DEVICE}"
    logger.info("Topic which will be published to: %s", TOPIC)
    
    # Initialize the MQTT client with the broker details
    mqtt_client = MQTTClient(MQTT_HOST, MQTT_PORT, MQTT_ENABLE_SSL, MQTT_USER, MQTT_PASSWORD)

    try:
        # Connect to the MQTT broker
        mqtt_client.connect()

        while True:
            try:
                # Call the barcode_reader function
                barcode_data = barcode_reader()

                # Log the scanned barcode
                logger.info("Scanned barcode: %s", barcode_data)

                # Get the current timestamp
                timestamp = time.time()
                
                # Publish the barcode data to an MQTT topic
                mqtt_client.client.publish(topic=TOPIC, payload=f"{barcode_data} [{timestamp}]", qos=0, retain=False)

            except KeyboardInterrupt:
                # Handle Keyboard Interrupt to exit the program
                logger.info("Keyboard interrupt detected. Exiting...")
                break

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
     main()

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

import json
import time
import sys
from readLogConfig import configure_logging_from_file
from opcUAserver.src.opcuaClient import MQTTClient
from readConfig import read_configuration


def main():
    # Initialize logger
    logger = configure_logging_from_file()

    # Read configuration from config.json
    config_file_path = '/mqttPub/data/config.json'  # Update with your config file path
    config_data = read_configuration(config_file_path)

    # Check if the configuration file can be read, else quit
    if config_data is None:
        logger.error("Failed to read configuration. Exiting...")
        sys.exit("Error: Failed to read the configuration. Program terminated.")

    # MQTT parameters
    MQTT_HOST = config_data.get("MQTT_HOST", {}).get("value")
    MQTT_PORT = config_data.get("MQTT_PORT", {}).get("value")
    MQTT_ENABLE_SSL = config_data.get("MQTT_ENABLE_SSL", {}).get("value")
    MQTT_USER = config_data.get("MQTT_USER", {}).get("value")
    MQTT_PASSWORD = config_data.get("MQTT_PASSWORD", {}).get("value")
    SUBSCRIBER_NAME = config_data.get("SUBSCRIBER_NAME", {}).get("value")
    SUBSCRIBER_DESCRIPTION = config_data.get("SUBSCRIBER_DESCRIPTION", {}).get("value")
    
    # Topic parameters
    DIVISION = config_data.get("DIVISION", {}).get("value")
    SITE = config_data.get("SITE", {}).get("value")
    BUILDING = config_data.get("BUILDING", {}).get("value")
    DEPARTMENT = config_data.get("DEPARTMENT", {}).get("value")
    MACHINE = config_data.get("MACHINE", {}).get("value")
    DEVICE = config_data.get("DEVICE", {}).get("value")

    # Create the MQTT topic
    TOPIC = f"{DIVISION}/{SITE}/{BUILDING}/{DEPARTMENT}/{MACHINE}/{DEVICE}"
    logger.info(f"Topic which will be published to: {TOPIC}")

    # Initialize the MQTT client
    mqtt_client = MQTTClient(MQTT_HOST, MQTT_PORT, MQTT_ENABLE_SSL, MQTT_USER, MQTT_PASSWORD)

    # Read variables from variables.json before entering the while loop
    variables_json_path = '/mqttPub/data/messages.json'  # Update with your variables JSON file path
    with open(variables_json_path, 'r') as f:
        variables_json = json.load(f)

    try:
        # Connect to the MQTT broker
        mqtt_client.connect()

        while True:
            try:
                for category in variables_json:
                    for item in variables_json[category]:
                        topic = item['topic']
                        variable = item['payload']['variable']
                        unit = item['payload']['unit']
                        value = eval(item['payload']['value'])  # Using eval to evaluate the random function
                        payload = f"{variable}: {value} {unit}"

                        # Debugging statement
                        logger.debug(f"Publishing to {topic}: {payload}")

                        # Publish to MQTT topic
                        mqtt_client.client.publish(topic=topic, payload=payload, qos=0, retain=False)

                # Add a sleep time to regulate the data sending rate
                time.sleep(1)

            except KeyboardInterrupt:
                # Handle Keyboard Interrupt to exit the program
                logger.info("Keyboard interrupt detected. Exiting...")
                break

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()

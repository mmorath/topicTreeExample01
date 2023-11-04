#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import json
import re
import sys
from readLogConfig import configure_logging_from_file
from mqttClient import MQTTClient
from readConfig import read_configuration


# Constants
CONFIG_FILE_PATH = '/app/data/conf.json'


# Function to sanitize topic components
def sanitize_topic_component(component):
    """
    Sanitizes the topic component to ensure it contains no uppercase letters,
    spaces, or special characters, replacing them with underscores.
    :param component: A string representing a single component of the MQTT topic.
    :return: A sanitized string with only lowercase letters, numbers, and underscores.
    """
    component = component.lower()
    component = re.sub(r'[^a-z0-9_]+', '_', component)
    return component


def main():
    # Initialize logger
    logger = configure_logging_from_file()

    # Read configuration from the standard path
    try:
        config_data = read_configuration(CONFIG_FILE_PATH)
    except json.JSONDecodeError as e:
        logger.error(f"Error: Invalid JSON format in the configuration file at {CONFIG_FILE_PATH} - {e}")
        sys.exit(1)  # Exit code 1 for general errors

    # Ensure the configuration data is not None
    if config_data is None:
        logger.error(f"Failed to read configuration from {CONFIG_FILE_PATH}. Exiting...")
        sys.exit(1)

    # Extract MQTT configuration with defaults
    mqtt_config = config_data.get("MQTT", {})
    MQTT_HOST = mqtt_config.get("HOST", "localhost")
    MQTT_PORT = int(mqtt_config.get("PORT", 1883))
    MQTT_ENABLE_SSL = mqtt_config.get("ENABLE_SSL", False)
    MQTT_USER = mqtt_config.get("USER", "")
    MQTT_PASSWORD = mqtt_config.get("PASSWORD", "")  # Sensitive, handle with care

    # Extract subscriber configuration with defaults
    subscriber_config = config_data.get("SUBSCRIBER", {})
    SUBSCRIBER_NAME = subscriber_config.get("NAME", "default_subscriber")
    SUBSCRIBER_DESCRIPTION = subscriber_config.get("DESCRIPTION", "Default MQTT Subscriber Description")

    # Log MQTT configuration while hiding sensitive information
    logger.info("MQTT Configuration:")
    logger.info(f"Host: {MQTT_HOST}")
    logger.info(f"Port: {MQTT_PORT}")
    logger.info(f"SSL Enabled: {MQTT_ENABLE_SSL}")
    logger.info(f"User: {MQTT_USER}")
    logger.info("Password: [HIDDEN]")
    logger.info(f"Subscriber Name: {SUBSCRIBER_NAME}")
    logger.info(f"Subscriber Description: {SUBSCRIBER_DESCRIPTION}")

    # Read and sanitize topic components
    topic_components = [
        sanitize_topic_component(comp) for comp in config_data.get("TOPIC_STRUCTURE", [])
    ]

    # Log each sanitized topic component to verify correctness
    logger.info("Sanitized Topic Components:")

    # Build the MQTT topic by joining the sanitized components with '/'
    TOPIC = '/'.join(topic_components)
    logger.info(f"Sanitized Full Topic Path: {TOPIC}")

    # Initialize the MQTT client (placeholder, implement accordingly)
    mqtt_client = MQTTClient(MQTT_HOST, MQTT_PORT, MQTT_ENABLE_SSL, MQTT_USER, MQTT_PASSWORD)

    # The rest of your code to connect to the broker and publish messages would go here
    # ...


if __name__ == "__main__":
    main()

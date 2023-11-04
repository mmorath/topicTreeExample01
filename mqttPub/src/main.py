#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import json
import re
import sys
import random
import string
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


# Function to safely generate a random message value
def evaluate_message_value(item):
    """
    Generate a random or default value for the message based on its type and constraints.
    If the type is not recognized, return an error message as the value.
    
    :param item: A dictionary containing the message definition including type and constraints.
    :return: A value for the message, or an error string if type is unrecognized.
    """
    value_type = item.get('type')
    try:
        if value_type == 'integer':
            return random.randint(item.get('min', 0), item.get('max', 100))
        elif value_type == 'string':
            return item.get('default', ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)))
        elif value_type == 'boolean':
            return random.choice([True, False])
        elif value_type == 'enum':
            return random.choice(item['enum'])
        elif value_type == 'float':
            min_val = item.get('min', 0.0)
            max_val = item.get('max', 100.0)
            return round(random.uniform(min_val, max_val), item.get('precision', 2))
        else:
            # If the type is not recognized, return an error message as the value
            return "Error: Unrecognized type"
    except (KeyError, ValueError, TypeError) as e:
        # If there are any issues with the parameters provided, return an error message
        return f"Error: {e}"


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
    # Initialize the MQTT client
    mqtt_client = MQTTClient(
        MQTT_HOST,
        MQTT_PORT,
        MQTT_ENABLE_SSL,
        MQTT_USER,
        MQTT_PASSWORD)

    # Connect to the MQTT broker
    try:
        mqtt_client.connect()

        # Process each message as per the 'MESSAGES' key in the configuration
        messages_config = config_data.get('MESSAGES', [])
        for message in messages_config:
            topic = TOPIC  # Assuming you want to publish each message on the same TOPIC
            name = message['name']
            value = evaluate_message_value(message)
            unit = message['unit']
            payload = f"{name}: {value} {unit}"

            # Debugging statement
            logger.debug(f"Publishing to {topic}: {payload}")

            # Publish to MQTT topic
            mqtt_client.publish(topic=topic, payload=payload, qos=0, retain=False)
            # Add a sleep time to regulate the data sending rate
            time.sleep(1)

    except KeyboardInterrupt:
        # Handle Keyboard Interrupt to exit the program
        logger.info("Keyboard interrupt detected. Exiting...")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()

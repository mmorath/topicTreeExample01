#!/usr/bin/env python
# -*- coding:utf-8 -*-

# =============================================================================
__author__ = "Matthias Morath"
__copyright__ = "Copyright 2023"
__credits__ = ["Matthias Morath"]
__license__ = "GPL"
__version__ = "2.0"
__maintainer__ = "Matthias Morath"
__email__ = "kompass_eng_0x@icloud.com"
__status__ = "Development"
# =============================================================================

import json
import random
import re
import string
import sys
import time
# from datetime import datetime
from readLogConfig import configure_logging_from_file
from mqttClient import MQTTClient
from readConfig import read_configuration


# Constants
CONFIG_FILE_PATH = '/app/data/conf.json'

# ==============================================================================
# Function to sanitize topic components
# ==============================================================================


def sanitize_topic_component(component):
    """
    Sanitizes the topic component to ensure it contains no uppercase letters,
    spaces, or special characters, replacing them with underscores.

    :param component: A string representing a single component of the
                      MQTT topic.
    :return: A sanitized string with only lowercase letters, numbers,
             and underscores.
    """
    component = component.lower()
    component = re.sub(r'[^a-z0-9_]+', '_', component)
    return component

# ==============================================================================
# Function to safely generate a random message value
# ==============================================================================


def evaluate_message_value(item):
    """
    Generate a random or default value for the message based on its type and
    constraints. If the type is not recognized, return an error message as the
    value.

    :param item: Dict containing the message definition including type and
                 constraints.
    :return: Value for the message, or an error string if type is unrecognized.
    """
    if 'default' in item:
        return item['default']
    else:
        # If there is no 'default', generate a random value
        return generate_random_value(item)

def generate_random_value(item):
    value_type = item.get('type')
    try:
        if value_type == 'integer':
            return random.randint(item.get('min', 0), item.get('max', 100))
        elif value_type == 'string':
            return item.get('default', ''.join(random.choices(
                string.ascii_uppercase + string.digits, k=10)))
        elif value_type == 'boolean':
            return random.choice([True, False])
        elif value_type == 'enum':
            return random.choice(item['enum'])
        elif value_type == 'float':
            min_val = item.get('min', 0.0)
            max_val = item.get('max', 100.0)
            return round(random.uniform(min_val, max_val), item.get('precision', 2))
        else:
            logging.error(f"Unrecognized type: {value_type}")
            return None  # or raise an exception
    except (KeyError, ValueError, TypeError) as e:
        logging.error(f"Error generating value for {item}: {e}")
        return None  # or raise an exception

# ==============================================================================
# Function to build a JSON-formatted payload for MQTT messages
# ==============================================================================


def build_topic_payload(variable, value, unit):
    """
    Constructs a JSON-formatted payload for an MQTT message including a
    timestamp and the given variable information.

    :param variable: The name of the variable.
    :param value: The value to send.
    :param unit: The unit of the value.
    :return: A JSON-formatted string payload.
    """
    payload = {
        # 'timestamp': int(time.time()),
        # 'timestamp_readable': datetime.utcnow().strftime(
        #     "%d-%m-%Y %H:%M:%S.%f")[:-3] + "Z",
        'variable': variable,
        'value': value,
        'unit': unit,
    }
    return json.dumps(payload)

# ==============================================================================
# Main function
# ==============================================================================


def main():
    """ Main function for publishing MQTT messages. """
    logger = configure_logging_from_file()

    # Load and validate configuration
    try:
        config_data = read_configuration(CONFIG_FILE_PATH)
    except json.JSONDecodeError as e:
        logger.error("Invalid JSON format in config: %s - %s",
                     CONFIG_FILE_PATH, e)
        sys.exit(1)

    if config_data is None:
        logger.error("Failed to read config: %s. Exiting...",
                     CONFIG_FILE_PATH)
        sys.exit(1)

    # MQTT configuration
    mqtt_config = config_data.get("MQTT", {})
    MQTT_HOST = mqtt_config.get("HOST", "localhost")
    MQTT_PORT = int(mqtt_config.get("PORT", 1883))
    MQTT_ENABLE_SSL = mqtt_config.get("ENABLE_SSL", False)
    MQTT_USER = mqtt_config.get("USER", "")
    MQTT_PASSWORD = mqtt_config.get("PASSWORD", "")

    # Subscriber configuration
    subscriber_config = config_data.get("SUBSCRIBER", {})
    SUBSCRIBER_NAME = subscriber_config.get("NAME", "default_subscriber")
    SUBSCRIBER_DESCRIPTION = subscriber_config.get("DESCRIPTION",
                                                   "Default MQTT Subscriber")

    logger.info("MQTT Configuration:")
    logger.info(f"Host: {MQTT_HOST}")
    logger.info(f"Port: {MQTT_PORT}")
    logger.info(f"SSL Enabled: {MQTT_ENABLE_SSL}")
    logger.info(f"User: {MQTT_USER}")
    logger.info("Password: [HIDDEN]")
    logger.info(f"Publisher Name: {SUBSCRIBER_NAME}")
    logger.info(f"Publisher Description: {SUBSCRIBER_DESCRIPTION}")

    # Topic construction
    topic_components = [
        sanitize_topic_component(comp) for comp in config_data.get(
            "TOPIC_STRUCTURE", [])
    ]
    TOPIC = '/'.join(topic_components)
    logger.info(f"Sanitized Full Topic Path: {TOPIC}")

    mqtt_client = MQTTClient(
        mqtt_host=MQTT_HOST,
        mqtt_port=MQTT_PORT,
        mqtt_enable_ssl=MQTT_ENABLE_SSL,
        mqtt_user=MQTT_USER,
        mqtt_password=MQTT_PASSWORD,
        subscriber_name=SUBSCRIBER_NAME)

    mqtt_client.connect()

    while not mqtt_client.flag_connected:
        logger.info("Waiting for MQTT client to connect...")
        time.sleep(1)

    # Message processing
    messages_config = config_data.get('MESSAGES', [])
    try:
        while True:
            for message in messages_config:
                message_name = message['name']
                message_topic = f"{TOPIC}/{message_name}"
                value = evaluate_message_value(message)
                unit = message.get('unit', '')
                payload = build_topic_payload(message_name, value, unit)

                #logger.info(f"Publishing to {message_topic}: {payload}")
                mqtt_client.publish(topic=message_topic, payload=payload,
                                    qos=0, retain=False)

                time.sleep(1)

            if not mqtt_client.flag_connected:
                logger.error("Lost connection to broker. Exiting...")
                break

    except KeyboardInterrupt:
        mqtt_client.disconnect()
        logger.info("Keyboard interrupt detected. Exiting...")
    except Exception as e:
        mqtt_client.disconnect()
        logger.error("An error occurred: %s", e)


if __name__ == "__main__":
    main()

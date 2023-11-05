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
import sys
import time
from readLogConfig import configure_logging_from_file
from mqttClient import MQTTClient
from readConfig import read_configuration

# Constants
CONFIG_FILE_PATH = '/app/data/conf.json'

# ==============================================================================
# Main function
# ==============================================================================


def on_message(client, userdata, message):
    """ Callback function for when a message is received. """
    payload = str(message.payload.decode("utf-8"))
    logger.info(f"Message received: topic='{message.topic}' payload='{payload}'")


def main():
    """ Main function for subscribing to MQTT topics. """
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

    # Topics to subscribe
    topics = config_data.get("TOPICS", [])

    logger.info("Starting MQTT Subscriber...")
    logger.info(f"Subscriber Name: {SUBSCRIBER_NAME}")
    logger.info(f"Subscriber Description: {SUBSCRIBER_DESCRIPTION}")

    mqtt_client = MQTTClient(
        mqtt_host=MQTT_HOST,
        mqtt_port=MQTT_PORT,
        mqtt_enable_ssl=MQTT_ENABLE_SSL,
        mqtt_user=MQTT_USER,
        mqtt_password=MQTT_PASSWORD,
        subscriber_name=SUBSCRIBER_NAME)

    # Set the on_message callback and connect to broker
    mqtt_client.on_message = on_message
    mqtt_client.connect()

    while not mqtt_client.flag_connected:
        logger.info("Waiting for MQTT client to connect...")
        time.sleep(1)

    # Subscribing to topics
    for topic_info in topics:
        topic = topic_info["TOPIC"]
        qos = topic_info.get("qos", 0)
        logger.info(f"Subscribing to topic: {topic} with QoS {qos}")
        mqtt_client.subscribe(topic, qos)

    # Start the network loop
    try:
        mqtt_client.loop_forever()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt detected. Exiting...")
    except Exception as e:
        logger.error("An error occurred: %s", e)
    finally:
        mqtt_client.disconnect()


if __name__ == "__main__":
    main()

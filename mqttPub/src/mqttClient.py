#!/usr/bin/env python
# -*- coding:utf-8 -*-

import paho.mqtt.client as mqttPubSub
import time
import logging


class MQTTClient:
    def __init__(
            self,
            mqtt_host,
            mqtt_port,
            mqtt_enable_ssl,
            mqtt_user,
            mqtt_password,
            subscriber_name):
        self.mqtt_host = mqtt_host
        self.mqtt_port = mqtt_port
        self.mqtt_enable_ssl = mqtt_enable_ssl
        self.mqtt_user = mqtt_user
        self.mqtt_password = mqtt_password
        self.client = mqttPubSub.Client(
            client_id=subscriber_name,
            userdata=None,
            protocol=mqttPubSub.MQTTv5)
        self.flag_connected = False

    def connect(self):
        try:
            if self.mqtt_enable_ssl:
                self.client.tls_set(tls_version=mqttPubSub.ssl.PROTOCOL_TLS)
                self.client.username_pw_set(self.mqtt_user, self.mqtt_password)

            # Set the callback functions
            self.client.on_connect = self.on_connect
            self.client.on_disconnect = self.on_disconnect
            self.client.on_subscribe = self.on_subscribe
            self.client.on_message = self.on_message
            self.client.on_log = self.on_log

            # Connect to the MQTT broker
            self.client.connect(self.mqtt_host, self.mqtt_port)
            logging.info(
                'Connecting to MQTT broker: %s on port: %s',
                self.mqtt_host,
                self.mqtt_port)
            self.client.loop_start()

        except Exception as e:
            logging.error(f"Error connecting to MQTT broker: {str(e)}")
            # Retry connection after a delay
            time.sleep(10)
            self.connect()  # Retry connection

    def on_connect(self, client, userdata, flags, rc, properties=None):
        """ callback on connect """
        if rc == 0:
            self.flag_connected = True
            logging.info(
                'Connected successfully to MQTT host: %s on port: %s',
                self.mqtt_host,
                self.mqtt_port)
        else:
            self.flag_connected = False
            logging.error(
                'No connection to MQTT host: %s on port: %s,'
                ' returned result code: %s',
                self.mqtt_host,
                self.mqtt_port,
                str(rc))

    def on_disconnect(self, client, userdata, rc):
        """ callback on disconnect """
        logging.info(
            'Disconnected from MQTT host: %s on port: %s with result code: %s',
            self.mqtt_host,
            self.mqtt_port,
            str(rc))
        client.loop_stop()

    def on_subscribe(
            self,
            client,
            userdata,
            mid,
            granted_qos,
            properties=None):
        """ callback on subscribe """
        logging.info("Subscribed: %s %s", str(mid), str(granted_qos))

    def on_message(self, client, userdata, msg):
        """ callback on message for when a PUBLISH message is received
        from the server """
        payload = str(msg.payload.decode("utf-8"))
        logging.info(
            'Received topic: %s payload: %s qos: %s retain: %s',
            msg.topic,
            payload,
            msg.qos,
            msg.retain)

    def on_log(self, client, userdata, level, buf):
        """ callback for logging """
        logging.debug('%s', buf)

    def publish(self, topic, payload, qos=0, retain=False):
        """
        Publish a message to a topic on the MQTT broker.
        :param topic: The topic to publish to.
        :param payload: The message payload to publish.
        :param qos: The Quality of Service level of the message.
        :param retain: If True, the message will be set as the
                        "last known good" for the topic.
        """
        if self.flag_connected:  # Only attempt to publish if connected
            self.client.publish(topic, payload, qos, retain)
        else:
            logging.error("Cannot publish because the client is not "
                          "connected.")

    def disconnect(self):
        """ Disconnect from the MQTT broker. """
        if self.flag_connected:
            logging.info("Disconnecting from broker")
            self.client.disconnect()
            self.flag_connected = False
        else:
            logging.warning("Attempted to disconnect when not connected")

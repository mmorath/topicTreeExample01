#!/usr/bin/env python
# -*- coding:utf-8 -*-

import paho.mqtt.client as mqtt
import logging

class MQTTClient:
    def __init__(self, mqtt_host, mqtt_port, mqtt_enable_ssl, mqtt_user,
                 mqtt_password, subscriber_name):
        self.mqtt_host = mqtt_host
        self.mqtt_port = mqtt_port
        self.mqtt_enable_ssl = mqtt_enable_ssl
        self.mqtt_user = mqtt_user
        self.mqtt_password = mqtt_password
        self.client = mqtt.Client(client_id=subscriber_name,
                                  clean_session=True)
        self.flag_connected = False

        # Set the callback functions
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message
        self.client.on_log = self.on_log

        if self.mqtt_enable_ssl:
            # Add arguments if necessary (certs, keys, etc.)
            self.client.tls_set()

        self.client.username_pw_set(self.mqtt_user, self.mqtt_password)

    def connect(self):
        try:
            # Connect to the MQTT broker
            self.client.connect(self.mqtt_host, self.mqtt_port)
            logging.info('Connecting to MQTT broker: %s on port: %s',
                         self.mqtt_host, self.mqtt_port)
            self.client.loop_start()

        except Exception as e:
            logging.error("Error connecting to MQTT broker: %s", str(e))
            # Retry connection or handle reconnection logic here

    def on_connect(self, client, userdata, flags, rc):
        """ Callback on connect """
        if rc == 0:
            self.flag_connected = True
            logging.info('Connected successfully to MQTT host: %s on port: %s',
                         self.mqtt_host, self.mqtt_port)
        else:
            self.flag_connected = False
            logging.error('Failed to connect to MQTT host: %s on port: %s, '
                          'result code: %s', self.mqtt_host, self.mqtt_port, rc)

    def on_disconnect(self, client, userdata, rc):
        """ Callback on disconnect """
        self.flag_connected = False
        logging.info('Disconnected from MQTT host: %s on port: %s with '
                     'result code: %s', self.mqtt_host, self.mqtt_port, rc)
        client.loop_stop()

    def on_subscribe(self, client, userdata, mid, granted_qos):
        """ Callback on subscribe """
        logging.info("Subscribed: mid=%s qos=%s", str(mid), str(granted_qos))

    def on_message(self, client, userdata, msg):
        """ Callback on message when a PUBLISH message is received 
            from the server """
        logging.info('Received message on topic: %s with QoS %s: %s',
                     msg.topic, msg.qos, msg.payload.decode("utf-8"))

    def on_log(self, client, userdata, level, buf):
        """ Callback for logging """
        logging.debug('%s', buf)

    def subscribe(self, topic, qos=0):
        """ Subscribe to a topic on the MQTT broker. """
        if self.flag_connected:
            self.client.subscribe(topic, qos)
        else:
            logging.error("Cannot subscribe because the client is not "
                          "connected.")

    def publish(self, topic, payload, qos=0, retain=False):
        """ Publish a message to a topic on the MQTT broker. """
        if self.flag_connected:
            self.client.publish(topic, payload, qos, retain)
        else:
            logging.error("Cannot publish because the client is not "
                          "connected.")

    def disconnect(self):
        """ Disconnect from the MQTT broker. """
        self.client.disconnect()

import sys
import time
import json
import random
import logging
import asyncio
from opcua import Server
from datetime import datetime

class OPCUAServer:
    """OPC-UA Server to provide OPC-UA services.

    This class initializes an OPC-UA server and allows for serving
    variables based on a JSON configuration.

    Attributes:
        endpoint (str): The endpoint URL for the OPC-UA server.
        server (Server): Instance of the Server class from opcua library.
    """

    def __init__(self, endpoint, logger):
        """
        Initialize the OPCUAServer with the given endpoint.

        Args:
            endpoint (str): The endpoint URL for the OPC-UA server.
            logger (logging.Logger): Logger instance for logging messages.
        """
        self.endpoint = endpoint
        self.logger = logger
        self.server = Server()
        self.server.set_endpoint(self.endpoint)

    async def load_variables_from_json(self, json_file):
        """
        Load and serve variables based on a JSON configuration.

        Args:
            json_file (str): The path to the JSON file with variable configurations.

        Returns:
            None
        """
        try:
            with open(json_file, 'r') as f:
                config = json.load(f)

            for var in config['variables']:
                idx = self.server.get_namespace_index(var['namespace']) if self.server.get_namespace_index(var['namespace']) != -1 else self.server.register_namespace(var['namespace'])
                obj = self.server.nodes.objects.add_object(idx, var['name'])
                value = random.uniform(var['min_value'], var['max_value'])
                obj.add_variable(idx, var['identifier'], value, var_type=var['identifier_type'])

        except Exception as e:
            self.logger.error(f"Error loading variables from JSON: {str(e)}")

    def start(self):
        """
        Start the OPC-UA server.

        Returns:
            None
        """
        try:
            self.server.start()
            self.logger.info(f"OPC-UA Server started at {self.endpoint}")
        except Exception as e:
            self.logger.error(f"Error starting the OPC-UA server: {str(e)}")

    def stop(self):
        """
        Stop the OPC-UA server.

        Returns:
            None
        """
        try:
            self.server.stop()
            self.logger.info("OPC-UA Server stopped.")
        except Exception as e:
            self.logger.error(f"Error stopping the OPC-UA server: {str(e)}")

       
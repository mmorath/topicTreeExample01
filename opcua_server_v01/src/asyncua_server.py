import json
import random
import logging
import asyncio
from asyncua import Server

class OPCUAServer:
    """
    OPC-UA Server to provide OPC-UA services.

    This class initializes an OPC-UA server and allows for serving
    variables based on a JSON configuration.

    Attributes:
        endpoint (str): The endpoint URL for the OPC-UA server.
        server (Server): Instance of the Server class from the asyncua library.
        logger (logging.Logger): Logger instance for logging messages.
    """
    
    def __init__(self, endpoint, logger):
        """
        Initialize the OPCUAServer with the given endpoint and logger.

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
            # Attempt to open the JSON file
            with open(json_file, 'r') as f:
                config = json.load(f)

            # Loop through the variables in the JSON file
            for var in config['variables']:
                idx = await self.server.register_namespace(var['namespace'])
                obj = await self.server.nodes.objects.add_object(idx, var['name'])
                value = random.uniform(var['min_value'], var['max_value'])
                
                # Add the variable to the OPC-UA server
                await obj.add_variable(idx, var['identifier'], value)
                
            self.logger.info("Successfully loaded variables from JSON.")

        except Exception as e:
            self.logger.error(f"Error loading variables from JSON: {str(e)}")
            self.logger.debug(f"Exception details: {e}")

    async def start(self):
        """
        Start the OPC-UA server.

        Returns:
            None
        """
        try:
            await self.server.start()
            self.logger.info(f"OPC-UA Server started at {self.endpoint}")
        except Exception as e:
            self.logger.error(f"Error starting the OPC-UA server: {str(e)}")
            self.logger.debug(f"Exception details: {e}")

    async def stop(self):
        """
        Stop the OPC-UA server.

        Returns:
            None
        """
        try:
            await self.server.stop()
            self.logger.info("OPC-UA Server stopped successfully.")
        except Exception as e:
            self.logger.error(f"Error stopping the OPC-UA server: {str(e)}")
            self.logger.debug(f"Exception details: {e}")
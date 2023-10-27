import sys
import time
import json
import random
import logging
import asyncio
from opcua import Server
from datetime import datetime

# Constants
SERVER_NAME = "YourServerName"  # Replace with your server name

class OPCUAServer:
    """OPC-UA Server to provide OPC-UA services.

    This class serves OPC-UA variables based on a JSON configuration.

    Attributes:
        endpoint (str): Endpoint URL for the server.
        server (Server): Instance of the Server class from opcua library.
    """

    def __init__(self, endpoint):
        """Initialize the OPCUAServer.

        Args:
            endpoint (str): The endpoint URL for the OPC-UA server.
        """
        self.endpoint = endpoint
        self.server = Server()
        self.server.set_endpoint(self.endpoint)

    async def load_variables_from_json(self, json_file):
        """Load and serve variables based on JSON configuration.

        Args:
            json_file (str): Path to the JSON file with variable configurations.

        Returns:
            None
        """
        try:
            with open(json_file, 'r') as f:
                config = json.load(f)

            # Serve variables
            for var in config['variables']:
                # Create or fetch the namespace
                idx = self.server.get_namespace_index(var['namespace']) if self.server.get_namespace_index(var['namespace']) != -1 else self.server.register_namespace(var['namespace'])

                # Create object to contain all variables
                obj = self.server.nodes.objects.add_object(idx, var['name'])

                # Serve variables with random initial value within specified range
                value = random.uniform(var['min_value'], var['max_value'])
                obj.add_variable(idx, var['identifier'], value, var_type=var['identifier_type'])

        except Exception as e:
            logging.error(f"Error loading variables from JSON: {str(e)}")

    def start(self):
        """Start the OPC-UA server."""
        try:
            self.server.start()
            logging.info(f"OPC-UA Server started at {self.endpoint}")
        except Exception as e:
            logging.error(f"Error starting the OPC-UA server: {str(e)}")

    def stop(self):
        """Stop the OPC-UA server."""
        try:
            self.server.stop()
            logging.info(f"OPC-UA Server stopped.")
        except Exception as e:
            logging.error(f"Error stopping the OPC-UA server: {str(e)}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    endpoint = "opc.tcp://localhost:4840/freeopcua/server/"
    json_file = "variables.json"

    server = OPCUAServer(endpoint)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(server.load_variables_from_json(json_file))

    try:
        server.start()
        loop.run_forever()

    except KeyboardInterrupt:
        server.stop()
        loop.close()

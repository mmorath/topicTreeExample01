import sys
import time
import logging
from opcua import Client, ua

# Constants
SUBSCRIBER_NAME = "YourSubscriberName"  # Replace with your subscriber name

class OPCUAClient:
    """OPC-UA Client to interact with an OPC-UA server.

    This class provides methods to connect, disconnect, read nodes, and
    write values to nodes on an OPC-UA server.

    Attributes:
        server_url (str): URL of the OPC-UA server.
        username (str): Username for server authentication.
        password (str): Password for server authentication.
        client (Client): Instance of the Client class from opcua library.
        flag_connected (bool): Flag to indicate the connection status.
    """

    def __init__(self, server_url, username=None, password=None):
        """Initialize the OPCUAClient.

        Args:
            server_url (str): The URL of the OPC-UA server to connect to.
            username (str, optional): The username for server authentication.
            password (str, optional): The password for server authentication.
        """
        self.server_url = server_url
        self.username = username
        self.password = password
        self.client = Client(self.server_url)
        self.flag_connected = False

    def connect(self):
        """Connect to the OPC-UA server."""
        try:
            # User authentication
            if self.username and self.password:
                self.client.set_user(self.username)
                self.client.set_password(self.password)

            # Perform the connection
            self.client.connect()
            logging.info(f"Connected to OPC-UA server at {self.server_url}")
            self.flag_connected = True
        except Exception as e:
            logging.error(f"Error connecting to OPC-UA server: {str(e)}")
            # Retry connection with a delay
            time.sleep(10)
            self.connect()  # Recursive retry

    def disconnect(self):
        """Disconnect from the OPC-UA server."""
        try:
            self.client.disconnect()
            logging.info(f"Disconnected from OPC-UA server at {self.server_url}")
            self.flag_connected = False
        except Exception as e:
            logging.error(f"Error disconnecting from OPC-UA server: {str(e)}")

    def read_node(self, node_id):
        """Read value from a node in the OPC-UA server.

        Args:
            node_id (str): The node ID to read from.

        Returns:
            any: The value of the node. Returns None if read operation fails.
        """
        try:
            if self.flag_connected:
                node = self.client.get_node(node_id)
                return node.get_value()
        except Exception as e:
            logging.error(f"Error reading node {node_id}: {str(e)}")
            return None

    def write_node(self, node_id, value):
        """Write a value to a node in the OPC-UA server.

        Args:
            node_id (str): The node ID to write to.
            value (any): The value to write.

        Returns:
            None
        """
        try:
            if self.flag_connected:
                node = self.client.get_node(node_id)
                node.set_value(value)
        except Exception as e:
            logging.error(f"Error writing to node {node_id}: {str(e)}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    server_url = "opc.tcp://localhost:4840/freeopcua/server/"
    username = None
    password = None

    client = OPCUAClient(server_url, username, password)
    client.connect()

    try:
        # Perform read and write operations here
        pass
    finally:
        client.disconnect()

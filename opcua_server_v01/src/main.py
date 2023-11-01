#!/usr/bin/env python
# -*- coding:utf-8 -*-

# =============================================================================
__author__ = "Matthias Morath"
__copyright__ = "Copyright 2021"
__credits__ = ["Matthias Morath"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Matthias Morath"
__email__ = "kompass_eng_0x@icloud.com"
__status__ = "Development"
# =============================================================================

import json
import sys
import asyncio
from readLogConfig import configure_logging_from_file
from readConfig import read_configuration
from opcuaServer import OPCUAServer  # Adjust this import based on your project's structure

# Define constants for file paths here for easy management
CONFIG_FILE_PATH = '/opcua_server_v01/data/config.json'
VARIABLES_JSON_PATH = '/opcua_server_v01/data/messages.json'

def main():
    # Initialize logger
    logger = configure_logging_from_file()
    if logger is None:
        sys.exit("Logger couldn't be configured. Exiting...")

    # Read configuration from JSON file
    config_data = read_configuration(CONFIG_FILE_PATH)

    if config_data is None:
        logger.error("Failed to read configuration. Exiting...")
        sys.exit("Error: Failed to read the configuration. Program terminated.")
    
    # OPC-UA server parameters
    OPCUA_ENDPOINT = config_data.get("OPCUA_ENDPOINT", {}).get("value", "opc.tcp://localhost:4840/freeopcua/server/")
    
    # Initialize the OPC-UA server
    opcua_server = OPCUAServer(OPCUA_ENDPOINT, logger)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(opcua_server.load_variables_from_json(VARIABLES_JSON_PATH))

    try:
        opcua_server.start()
        loop.run_forever()

    except KeyboardInterrupt:
        logger.info("Keyboard interrupt detected. Exiting...")
        opcua_server.stop()
        loop.close()

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
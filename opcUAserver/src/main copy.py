#!/usr/bin/env python
# -*- coding:utf-8 -*-

# =============================================================================
__author__ = "Matthias Morath"
__copyright__ = "Copyright 2021"
__credits__ = ["Matthias Morath"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Matthias Morath"
__email__ = "kompass_eng_0x@icloud.com"  kompass_eng_0x@icloud.com
__status__ = "Development"
# =============================================================================

import json
import sys
import asyncio
from readLogConfig import configure_logging_from_file
from readConfig import read_configuration
from opcUAserver.src.opcuaServer import OPCUAServer  # Replace with the actual path to your OPCUAServer file

def main():
    # Initialize logger
    logger = configure_logging_from_file()

    # Read configuration from config.json
    config_file_path = '/mqttPub/data/config.json'  # Update with your config file path
    config_data = read_configuration(config_file_path)

    # Check if the configuration file can be read, else quit
    if config_data is None:
        logger.error("Failed to read configuration. Exiting...")
        sys.exit("Error: Failed to read the configuration. Program terminated.")

    # OPC-UA server parameters
    OPCUA_ENDPOINT = config_data.get("OPCUA_ENDPOINT", {}).get("value", "opc.tcp://localhost:4840/freeopcua/server/")
    
    # Initialize the OPC-UA server
    opcua_server = OPCUAServer(OPCUA_ENDPOINT)

    # Read variables from variables.json before starting the OPC-UA server
    variables_json_path = '/mqttPub/data/variables.json'  # Update with your variables JSON file path
    loop = asyncio.get_event_loop()
    loop.run_until_complete(opcua_server.load_variables_from_json(variables_json_path))

    try:
        opcua_server.start()
        loop.run_forever()
        
    except KeyboardInterrupt:
        # Handle Keyboard Interrupt to exit the program
        logger.info("Keyboard interrupt detected. Exiting...")
        opcua_server.stop()
        loop.close()

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()

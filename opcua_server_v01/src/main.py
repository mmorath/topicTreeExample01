#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import json
import sys
import asyncio
from read_log_config import configure_logging_from_file
from read_config import read_configuration
from asyncua_server import AsyncUAServer

# Get the directory containing your script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Compute the absolute paths to your config files
LOGGER_FILE_PATH = os.path.join(script_dir, '..', 'data', 'logger.conf')
CONFIG_FILE_PATH = os.path.join(script_dir, '..', 'data', 'config.json')
VARIABLES_JSON_PATH = os.path.join(script_dir, '..', 'data', 'messages.json')

async def main():
    """
    Main function to initialize and run the asynchronous OPC-UA server.
    """
    
    # Try to initialize the logger
    try:
        logger = configure_logging_from_file(LOGGER_FILE_PATH)
        if logger is None:
            sys.exit("Error: Logger couldn't be configured. Exiting...")
        logger.info("Logger successfully initialized.")
    except Exception as e:
        sys.exit(f"Could not configure logger: {str(e)}")

    # Try to read the config    
    try:
        logger.info("Attempting to read configuration...")
        
        config = read_configuration(CONFIG_FILE_PATH)
        if config is None:
            logger.error("Failed to read configuration. Exiting...")
            sys.exit("Error: Failed to read the configuration. Program terminated.")
        
        logger.info("Successfully read configuration.")

        opcua_server_settings = config.get("OPCUA_SERVER_SETTINGS", {})
        endpoint = opcua_server_settings.get("endpoint", "opc.tcp://127.0.0.1:4840/opcua/")
        server_name = opcua_server_settings.get("server_name", "DevNet OPC-UA Test Server")
        namespace_uri = opcua_server_settings.get("namespace", {}).get("uri", "http://devnetiot.com/opcua/")
        
        logger.info(f"Server settings: endpoint={endpoint}, server_name={server_name}, namespace_uri={namespace_uri}")

        async_ua_server = AsyncUAServer(endpoint, logger)
        async_ua_server.set_server_name(server_name)
        await async_ua_server.register_namespace(namespace_uri)
        
        logger.info("Loading variables from JSON file...")
        await async_ua_server.load_variables_from_json(VARIABLES_JSON_PATH)
        logger.info("Variables successfully loaded.")

        try:
            logger.info("Starting the OPC-UA server...")
            await async_ua_server.start()
            logger.info("OPC-UA server started. Entering main loop...")
            while True:
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt detected. Exiting...")
            await async_ua_server.stop()
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())

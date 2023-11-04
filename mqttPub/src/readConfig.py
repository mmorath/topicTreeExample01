#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
import json
import traceback


def read_configuration(file_path):
    """
    Read the configuration data from a JSON file.

    Args:
        file_path (str): The path to the JSON configuration file.

    Returns:
        dict: The loaded configuration data if successful, None otherwise.
    """
    logger = logging.getLogger(__name__)

    try:
        logger.info(f"Reading configuration from file: {file_path}")
        with open(file_path, 'r') as file:
            config_data = json.load(file)
        logger.info("Configuration successfully read.")
        return config_data
    except FileNotFoundError:
        logger.error(f"Error: Configuration file not found at {file_path}")
    except json.JSONDecodeError as e:
        logger.error(f"""Error: Invalid JSON format in the configuration
                        file at {file_path} - {e}""")
    except Exception as e:
        logger.error(f"""An unexpected error occurred while reading the
                        configuration: {e}""")
        # This line will print the stack trace to the debug log
        logger.debug(traceback.format_exc())
    # If any exception was caught, None is returned
    return None

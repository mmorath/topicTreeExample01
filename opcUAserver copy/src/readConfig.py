import logging
import json

def read_configuration(file_path):
    """
    Read the configuration data from a JSON file.

    Args:
        file_path (str): The path to the JSON configuration file.

    Returns:
        dict: The loaded configuration data if successful, None otherwise.
    """
    logger = logging.getLogger(__name__)
    config_data = None

    try:
        logger.info(f"Reading configuration from file: {file_path}")
        with open(file_path, 'r') as file:
            config_data = json.load(file)

        logger.info("Configuration successfully read.")
        return config_data  # Return the loaded configuration data

    except FileNotFoundError:
        logger.error("Error: Configuration file not found.")
    except json.JSONDecodeError:
        logger.error("Error: Invalid JSON format in the configuration file.")
    except Exception as e:
        logger.error(f"Error: {str(e)}")

    return config_data  # Return None if there was an error reading the configuration

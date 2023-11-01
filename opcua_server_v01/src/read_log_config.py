import logging
import logging.handlers
import configparser
import ast  # for safely evaluating a string to create a Python object

def configure_logging_from_file(config_file_path):
    """
    Configure logging settings from a configuration file.
    
    Parameters:
        config_file_path (str): The path to the logging configuration file.

    Returns:
        logging.Logger: A configured logger instance.
    """
    try:
        # Read the logger configuration from file
        config = configparser.ConfigParser()
        config.read(config_file_path)

        # Create a logger using the configuration
        logger = logging.getLogger('myLogger')

        # Set the level for the logger
        logger.setLevel(logging.getLevelName(config.get('logger_myLogger', 'level')))

        # Create a syslog handler
        address = eval(config.get('handler_syslogHandler', 'args'))
        handler = logging.handlers.SysLogHandler(address=address)
        handler.setLevel(logging.getLevelName(config.get('handler_syslogHandler', 'level')))

        # Create a formatter
        formatter = logging.Formatter(config.get('formatter_simpleFormatter', 'format'), datefmt=config.get('formatter_simpleFormatter', 'datefmt'))

        # Set the formatter for the handler
        handler.setFormatter(formatter)

        # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)  # or whatever level you want for console output
        console_handler.setFormatter(formatter)

        # Add the handlers to the logger
        logger.addHandler(handler)
        logger.addHandler(console_handler)

        return logger

    except (configparser.Error, FileNotFoundError) as e:
        logging.basicConfig(level=logging.DEBUG)
        logging.warning(f"Failed to read logger configuration file: {str(e)}")
        logging.warning("Configuring basic logging.")
        return logging.getLogger()

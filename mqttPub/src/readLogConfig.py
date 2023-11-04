#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
import logging.handlers
import configparser


def configure_logging():
    # Create a logger
    logger = logging.getLogger('../data/logger.conf')

    # Set the level for the logger
    logger.setLevel(logging.DEBUG)

    # Create a handler
    handler = logging.handlers.SysLogHandler(
        address=('your_log_server_ip', 514))

    # Set the level for the handler
    handler.setLevel(logging.DEBUG)

    # Create a formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    # Set the formatter for the handler
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger


def configure_logging_from_file():
    try:
        # Read the logger configuration from file
        config = configparser.ConfigParser()
        config.read('/app/data/logger.conf')

        print("Logger configuration file successfully read.")

        # Create a logger using the configuration
        logger = logging.getLogger('myLogger')

        # Set the level for the logger
        logger.setLevel(
            logging.getLevelName(
                config.get(
                    'logger_myLogger',
                    'level')))

        # Create a handler
        address = eval(config.get('handler_syslogHandler', 'args'))
        handler = logging.handlers.SysLogHandler(address=address)

        # Set the level for the handler
        handler.setLevel(
            logging.getLevelName(
                config.get(
                    'handler_syslogHandler',
                    'level')))

        # Create a formatter
        formatter = logging.Formatter(
            config.get(
                'formatter_simpleFormatter', 'format'), datefmt=config.get(
                'formatter_simpleFormatter', 'datefmt'))

        # Set the formatter for the handler
        handler.setFormatter(formatter)

        # Add the handler to the logger
        logger.addHandler(handler)

        return logger

    except (configparser.Error, FileNotFoundError) as e:
        # If the configuration file cannot be read, configure basic logging
        logging.basicConfig(level=logging.DEBUG)
        logging.warning(f"Failed to read logger configuration file: {str(e)}")
        logging.warning("Configuring basic logging.")
        return logging.getLogger()

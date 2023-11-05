# mqttPub Project Structure
The `mqttPub` project is organized into various directories and files that 
hold the application code, configuration files, Docker components, 
and documentation. Here's the structure and the role of each item:

```bash
mqttPub/
├── Dockerfile            # Dockerfile to build the Docker image for the project
├── LICENSE.md            # The license file containing the terms of use and sharing
├── README.md             # The markdown file with instructions and documentation for the project
├── data                  # Directory containing the configuration files for different simulation scenarios
│   ├── conf_airpressure.json    # Configuration for air pressure simulation data
│   ├── conf_cooling.json        # Configuration for cooling system simulation data
│   ├── conf_exhaust.json        # Configuration for exhaust system simulation data
│   ├── conf_fit.json            # Configuration for fit mes simulation data
│   ├── conf_gas.json            # Configuration for gas system simulation data
│   ├── conf_iiot-box.json       # Configuration for IIoT box simulation data
│   ├── conf_mde.json            # Configuration for machine data entry (MDE) simulation
│   ├── conf_mes.json            # Configuration for manufacturing execution system (MES) simulation
│   ├── conf_power.json          # Configuration for power consumption simulation data
│   ├── logger.conf              # Logger configuration for the application
│   └── scanner.json             # Configuration for scanning-related simulation data
└── src                   # Source code directory for the MQTT simulation application
    ├── installEnv.sh           # Shell script to install the required environment for the app
    ├── main.py                 # Main Python script that runs the MQTT publisher simulation
    ├── mqttClient.py           # Python module handling MQTT client functionalities
    ├── readConfig.py           # Python module for reading configuration files
    ├── readLogConfig.py        # Python module to configure the logger
    └── requirements.txt        # Text file listing the Python dependencies for the project
```

## Detailed Description

### Dockerfile
Contains the instructions for Docker to build the environment in which the `mqttPub` application will run. This includes the base image, environment setup, and dependency installation.
### LICENSE.md
Holds the licensing agreement for the project. It's important to review this file to understand your rights and limitations for using the `mqttPub` project.
### README.md
The markdown document that you are currently reading. It includes setup instructions, a detailed description of the project, usage examples, and other important information for users and contributors.
### Data Directory
The `data` directory stores various JSON configuration files which are used to define different simulation scenarios for MQTT data publication. It allows for the customization of payloads and simulation parameters for each aspect of the IIoT environment the `mqttPub` is emulating.
### Source (src) Directory
This directory contains the actual Python code that makes up the application.

- `installEnv.sh`: A script for setting up the environment the Python application needs to run, including installing dependencies listed in `requirements.txt`.
- `main.py`: The entry point of the application which initializes the simulation and starts the publishing process.
- `mqttClient.py`: Defines the MQTT client logic for connecting to and interacting with the MQTT broker.
- `readConfig.py`: Provides functionality for reading and parsing configuration files from the `data` directory.
- `readLogConfig.py`: Sets up the logging configuration as specified in `logger.conf`.
- `requirements.txt`: Lists all the Python libraries that need to be installed for the application to run.

This structure and the files within are designed to provide a clear and maintainable architecture for developing and deploying the MQTT publishing simulation.
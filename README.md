# MQTT Topic Structure Example

Given your specific tag hierarchy, an MQTT topic for a cooling equipment sensor
on the machine bystronic01 located in room 035 on the first level of office
building n02 in building gb01 in the city ehingen (abbreviated eh) might look like this:

```bash
eh/gb01/n02/01/035/bystronic01/cooling
```
Here's what each part of the topic represents:

* <b>eh:</b> The city, Ehingen.<br>
* <b>gb01:</b> The building number 1.<br>
* <b>n02:</b> The office building number 2.<br>
* <b>01:</b> The first level of the building.<br>
* <b>035:</b> The room number.<br>
* <b>bystronic01:</b> The machine name and number.<br>
* <b>cooling:</b> The equipment type, in this case, a cooling system.

## Using Wildcards

With this structure in mind, let's consider a couple of scenarios using MQTT's wildcard characters:
Single-Level Wildcard +

Subscribe to any cooling equipment data on the first level of office building n02 in building gb01:

```bash
eh/gb01/n02/01/+/bystronic01/cooling
```

This would match:

    eh/gb01/n02/01/035/bystronic01/cooling
    eh/gb01/n02/01/036/bystronic01/cooling

And so on, for any room on the first level of office building n02 that has
a bystronic01 machine with cooling equipment.
Multi-Level Wildcard #

Subscribe to all sensor data related to the machine bystronic01 regardless of
its location within building gb01:

```bash
eh/gb01/#/bystronic01/cooling
```

This would match:

    eh/gb01/n02/01/035/bystronic01/cooling
    eh/gb01/n02/02/035/bystronic01/cooling
    eh/gb01/n03/01/010/bystronic01/cooling

And so on, for any bystronic01 machine's cooling equipment within building gb01.

Subscribe to all cooling equipment data within city eh:

```bash
eh/#/cooling
```
This would include cooling data from all buildings, levels, and rooms for any
machine within the city of Ehingen.

These examples show how MQTT topics and wildcards provide a flexible way to
organize and access data across an IIoT environment. By structuring your topics
logically and taking advantage of wildcards, you can simplify the process of data 
subscription and ensure that your clients receive all the relevant information they need.

## Testing and Simulating the MQTT Topic Structure

To properly test and simulate the MQTT topic structure, you will need to:

1. Have Docker and Docker Compose installed on your machine.
2. Configure your MQTT broker and the necessary simulation configurations in the `data` directory.
3. Build the Docker image and run the containers using Docker Compose.
4. Use an MQTT client to subscribe to topics and see the simulated messages.

### Prerequisites

Ensure that you have the following prerequisites installed:

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)

### Step 1: Configure MQTT Broker
First, you need to have an MQTT broker running and accessible. If you're using
a public broker or a broker that's already running within your network, 
make sure you have the connection details.

If you need to set up a local MQTT broker, you can do so using Docker. 
Here's a simple example using `eclipse-mosquitto`:

```yaml
# docker-compose.yml snippet for MQTT broker
services:
  mosquitto:
    image: eclipse-mosquitto:latest
    ports:
      - "1883:1883"
      - "9001:9001"
    volumes:
      - ./mosquitto/config:/mosquitto/config
      - ./mosquitto/data:/mosquitto/data
      - ./mosquitto/log:/mosquitto/log
```
Ensure you have the appropriate configuration files in the `./mosquitto/config` directory.

### Step 2: Configuration Files
Place your configuration JSON files within the `data` directory. Each file 
should represent a different aspect of the IIoT devices you're simulating.

### Step 3: Running Docker Compose
Navigate to the directory containing your `docker-compose.yml` file and run the
following command:

```bash
docker-compose up --build
```

This command will build the Docker image for the `mqttPub` application and start the services defined in `docker-compose.yml`.

### Step 4: Testing with MQTT Client

To test if the topics are being published correctly, you will need an MQTT client that can subscribe to the broker. You can use command-line tools like `mosquitto_sub` or GUI-based tools like MQTT Explorer.

Example using `mosquitto_sub` to subscribe to all topics with a wildcard:

```bash
mosquitto_sub -h <BROKER_HOST> -p <BROKER_PORT> -t 'eh/#' -v
```

This will listen for any messages published to topics that start with `eh/` and print them to the console.

## Validating Messages

After subscribing to the topics, you should start seeing messages from the `mqttPub` application in the MQTT client. Validate that:

- The topic structure matches your configuration.
- The payload of the messages is correct.
- All expected topics are being published to.

## Logs and Troubleshooting

If the messages are not appearing as expected, check the logs of the `mqttPub` application for any errors:

```bash
docker-compose logs mqttPub
```

Review the logs for any connectivity issues or configuration errors that could be preventing the publication of messages.

---

Replace `<BROKER_HOST>` and `<BROKER_PORT>` with the actual host and port of your MQTT broker.

Make sure to provide all necessary information about your broker and the `mqttPub` application setup to anyone using this README, so they can replicate the environment and test accordingly.

## Configuration and Setup Files

Our project utilizes Docker containers to manage various services. Configuration for these containers, along with the networking and logging setup, is defined through two primary files:
docker-services.json

This JSON file serves as the centralized configuration repository for our Docker services. It defines the MQTT broker details and a list of services with their specific configurations.

Structure:

    MQTT: Contains the connection details for the MQTT broker.
    services: An array of service configurations, where each service includes:
        service_name: The unique name for the service.
        hostname: The hostname assigned to the service's container.
        container_name: The container name used by Docker.
        config_path: The path to the configuration file for the service.
        username: The username for connecting to the MQTT broker.
        password: The password for MQTT broker authentication.

## How to generate the docker-compose.yml file

This file is pivotal for the script create_docker_compose_file.sh to generate the appropriate docker-compose.yml file.

```bash
create_docker_compose_file.sh
```

This shell script automates the creation of a docker-compose.yml calle "docker-compose_generated.yml" the file is based on the configurations defined in docker-services.json. It leverages the jq utility to parse JSON data.

Key Features:

1. Reads the docker-services.json configuration.
2. Dynamically constructs a docker-compose-generated.yml file
3. Assigns container names, hostnames, and volume mappings for each service.
4. Sets up network configurations for the Docker environment.
5. Applies logging options to keep the output manageable and relevant.

Usage:

To generate the docker-compose_generated.yml file, run the script:

```bash
./create_docker_compose_file.sh
```

Upon successful execution, docker-compose_generated.yml will be created or overwritten, which can then be used to start the Docker services with the command:

```bash
docker-compose -f docker-compose_generated.yml up
```

Do not forget to bring the services down...after testing
```bash
docker-compose -f docker-compose_generated.yml down
```
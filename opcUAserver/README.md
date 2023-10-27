# Scanner App

This project is a scanner application that interacts with a USB barcode scanner. It is designed to run within a Docker container.

## Requirements
- Docker

## Hardware 
### Raspberry pi
```bash
cat /proc/cpuinfo
...
Hardware        : BCM2835
Revision        : a02082
Serial          : 00000000e783636d
Model           : Raspberry Pi 3 Model B Rev 1.2
...
cat /etc/os-release
PRETTY_NAME="Raspbian GNU/Linux 11 (bullseye)"
NAME="Raspbian GNU/Linux"
VERSION_ID="11"
VERSION="11 (bullseye)"
VERSION_CODENAME=bullseye
ID=raspbian
ID_LIKE=debian
HOME_URL="http://www.raspbian.org/"
SUPPORT_URL="http://www.raspbian.org/RaspbianForums"
BUG_REPORT_URL="http://www.raspbian.org/RaspbianBugs"
```
### Scanner 
Scanner which was used in this example 

Honeywell Xenon MODEL: 1900

## Getting Started

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Build the Docker image:
   ```bash
    docker build -t scanner-app app
   ```
3. Run the Docker container
   ```bash
   docker run --privileged --cap-add=ALL --device=/dev/hidraw0 scanner-app
   ```
   The --privileged flag is used to give the container full access to the host system. The --cap-add=ALL flag allows the container to access all capabilities of the host. The --device=/dev/hidraw0 flag grants access to the USB barcode scanner device.

## Docker Compose
Alternatively, you can use Docker Compose to run the application. Make sure you have Docker Compose installed.
For this reason we do have a docker-compose file prepared 
   ```yml
    version: '3'

    services:
    scanner-app:
        build:
            context: ./app/
            dockerfile: Dockerfile
        privileged: true
        devices:
            - /dev/hidraw0
   ```
   Run the application using Docker Compose:
   ```bash
   docker-compose up
   ```
### What should you see 
   ```bash
    docker-compose build
    docker-compose up
    Creating network "raspiscanner_default" with the default driver
    Creating raspiscanner_scanner-app_1 ... done
    Attaching to raspiscanner_scanner-app_1
    scanner-app_1  | Logger configuration file successfully read.
    scanner-app_1  | WARNING:root:Failed to read logger configuration file: Bad value substitution: option 'format' in section 'formatter_simpleFormatter' contains an interpolation key 'asctime' which is not a valid option name. Raw value: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    scanner-app_1  | WARNING:root:Configuring basic logging.
    scanner-app_1  | INFO:readConfig:Reading configuration from file: /app/data/config.json
    scanner-app_1  | INFO:readConfig:Configuration successfully read.
    scanner-app_1  | INFO:root:Topic which will be published to: EMT/LHB/Halle2/assembly-line/torque-machine/barcode-scanner
    scanner-app_1  | DEBUG:root:Sending CONNECT (u1, p1, wr0, wq0, wf0, c1, k60) client_id=b'YourSubscriberName' properties=None
    scanner-app_1  | INFO:root:Connecting to MQTT broker: 2fec63f5313749619e6cadcd3272d557.s2.eu.hivemq.cloud on port: 8883
    scanner-app_1  | INFO:root:Initializing barcode reader...
    scanner-app_1  | DEBUG:root:Received CONNACK (0, Success) properties=[ReceiveMaximum : 10, TopicAliasMaximum : 5]
    scanner-app_1  | INFO:root:Connected successfully to MQTT host: 2fec63f5313749619e6cadcd3272d557.s2.eu.hivemq.cloud on port: 8883
    scanner-app_1  | INFO:root:Scanned barcode: 4006381333627
    scanner-app_1  | DEBUG:root:Sending PUBLISH (d0, q0, r0, m1), 'b'EMT/LHB/Halle2/assembly-line/torque-machine/barcode-scanner'', properties=None, ... (33 bytes)
    scanner-app_1  | INFO:root:Initializing barcode reader...
    scanner-app_1  | INFO:root:Scanned barcode: 4006381333627
    scanner-app_1  | DEBUG:root:Sending PUBLISH (d0, q0, r0, m4), 'b'EMT/LHB/Halle2/assembly-line/torque-machine/barcode-scanner'', properties=None, ... (33 bytes)
    scanner-app_1  | INFO:root:Initializing barcode reader...
    scanner-app_1  | INFO:root:Scanned barcode: 4017272282337
   ```

## Configuration

The application reads its configuration from the config.json file located in the data directory. Update this file with your desired configuration settings.

## Troubleshooting

If you encounter permission issues related to /dev/hidraw0, make sure that the user running the Docker container has the necessary permissions to access the USB device. Refer to the Docker documentation or your operating system's documentation for more information.
Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.

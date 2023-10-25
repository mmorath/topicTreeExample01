# Templates
This folder contains some templates to accelerate the development

## Some intresting ideas...links etc. 
Currently thinking about how to automize the docker container build using a docker-compose file. Would love to add some enviroment settings to the individual containers ...this would allow to modify for example the mqtt broker ...which is currently hard coded into the python start.py file. 

### using virtualenv...locally..wihout docker  
creating a postactivate hook 
explained here ... https://stackoverflow.com/questions/9554087/setting-an-environment-variable-in-virtualenv
```bash 
$ cat $VIRTUAL_ENV/bin/postactivate
#!/bin/bash
# This hook is run after this virtualenv is activated.
export NTP_HOST_01="" \
export NTP_HOST_02="" \
export MODBUS_TCP_HOST="" \
export MODBUS_TCP_PORT = "" \
export MODBUS_TCP_NAME = "pub" \
export MODBUS_TCP_MANUFACTURER ="topic" \
export MODBUS_TCP_DESCRIPTIPON ="test" \
export MODBUS_TCP_ORDER_NO ="" \
export MQTT_HOST="10.30.50.2"
export MQTT_PORT=1883
export MQTT_ENABLE_SSL=False
export MQTT_USER=""
export MQTT_PASSWORD=""
```

### dockerfile
```bash 
FROM python:3

#set enviroment variables 
ENV NTP_HOST_01="" \
    NTP_HOST_02="" \
    MODBUS_TCP_HOST="" \
    MODBUS_TCP_PORT = "" \
    MODBUS_TCP_NAME = "pub" \
    MODBUS_TCP_MANUFACTURER ="topic" \
    MODBUS_TCP_DESCRIPTIPON ="test" \
    MODBUS_TCP_ORDER_NO ="" \
    MQTT_HOST="10.30.50.2" \
    MQTT_PORT=1883 \
    MQTT_ENABLE_SSL=False \
    MQTT_USER="" \
    MQTT_PASSWORD="" \

#set working directory
WORKDIR /usr/src/app

#copy requirement file over
COPY requirements.txt ./

#run command
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./start.py" ]
```
Reading back the variables in python using OS module...
```bash 
import os
print(os.environ['DEVICE_HOST'])
```

### docker-compose
```bash 
version: "3.5"
services:
    # Iot box network switch 
    ie3400:
        build: ./cisco/ie3400/readout/
        hostname: ie3400
        container_name: ie3400
        environment:
            - NTP_HOST_01="" \
            - NTP_HOST_02="" \
            - MODBUS_TCP_IP_HOST="" \
            - MODBUS_TCP_PORT = "" \
            - MODBUS_TCP_NAME = "pub" \
            - MODBUS_TCP_MANUFACTURER ="topic" \
            - MODBUS_TCP_DESCRIPTIPON ="test" \
            - MODBUS_TCP_ORDER_NO ="" \
            - MQTT_HOST="10.30.50.2" \
            - MQTT_PORT=1883 \
            - MQTT_ENABLE_SSL=False \
            - MQTT_USER="" \
            - MQTT_PASSWORD="" \
        depends_on: 
            -mqttBroker
        networks: 
            -default    
        ports:
            - "1883:1883"
```

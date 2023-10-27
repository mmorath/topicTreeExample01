FROM python:3.7.3-alpine3.9

# This prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# This keeps Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED 1

# Install necessary packages
RUN apk update && apk add --no-cache \
    gfortran \
    libusb \
    libusb-dev

# Upgrade pip
RUN pip install --no-warn-script-location pip --upgrade

# Change working directory to /app
WORKDIR /app

# Copy requirement files
COPY  ./src/barcodeReader.py ./src/barcodeReader.py 
COPY  ./src/main.py ./src/main.py 
COPY  ./src/mqttClient.py ./src/mqttClient.py 
COPY  ./src/readConfig.py ./src/readConfig.py 
COPY  ./src/readLogConfig.py ./src/readLogConfig.py 
COPY  ./src/requirements.txt ./src/requirements.txt

# Copy data/config files
COPY ./data/logger.conf ./data/logger.conf
COPY ./data/config.json ./data/config.json

# Install the requirements
RUN pip install --no-warn-script-location -r ./src/requirements.txt

# Set the PATH to include the local bin directory
ENV PATH="/app/.local/bin:${PATH}"

# Add a label
LABEL maintainer="kompass_eng_0x@icloud.com" \
      version="1.0.0"

# Run the application
CMD [ "python", "./src/main.py" ]

# Use Python 3.7.3 based on Alpine 3.9
FROM python:3.7.3-alpine3.9

# Environment variables to prevent Python from writing pyc files and buffering stdin/stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Update and install necessary packages
RUN apk update && apk add --no-cache \
    gfortran \
    libusb \
    libusb-dev

# Upgrade pip
RUN pip install --upgrade pip

# Switch to working directory
WORKDIR /app

# Copy Python scripts
COPY ./src/installEnv.sh ./src/installEnv.sh
COPY ./src/installEnvV01.sh ./src/installEnvV01.sh
COPY ./src/main.py ./src/main.py
COPY ./src/opcuaServer.py ./src/opcuaServer.py
COPY ./src/readConfig.py ./src/readConfig.py
COPY ./src/readLogConfig.py ./src/readLogConfig.py
COPY ./src/requirements.txt ./src/requirements.txt

# Copy config files
COPY ./data/config.json ./data/config.json
COPY ./data/logger.conf ./data/logger.conf
COPY ./data/messages.json ./data/messages.json

# Install Python requirements
RUN pip install --no-cache-dir -r ./src/requirements.txt

# Add PATH environment variable
ENV PATH="/app/.local/bin:${PATH}"

# Metadata as described by labels
LABEL maintainer="kompass_eng_0x@icloud.com" \
      version="1.0.0"

# Run main.py when the container starts
CMD ["python", "./src/main.py"]

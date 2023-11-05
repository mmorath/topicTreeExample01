# Use an official lightweight Python image.
FROM python:3.7.3-alpine3.9

# Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1

# Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED 1

# Install necessary packages
RUN apk update && \
    apk add --no-cache --virtual .build-deps 

# Upgrade pip to latest version
RUN pip install --upgrade pip

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./src/ ./src/
COPY ./data/ ./data/

# Install any needed packages specified in requirements.txt
RUN pip install --no-warn-script-location -r ./src/requirements.txt && \
    # Remove the virtual build dependencies to reduce image size
    apk del .build-deps

# Set the PATH to include the local bin directory (if needed)
ENV PATH="/app/.local/bin:${PATH}"

# Add metadata to the image to describe that the maintainer is you
LABEL maintainer="kompass_eng_0x@icloud.com" \
      version="1.0.0"

# Run the application when the container launches
CMD ["python", "./src/main.py"]

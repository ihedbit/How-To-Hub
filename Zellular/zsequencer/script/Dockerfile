# Use the official Ubuntu 24.04 image as the base image
FROM ubuntu:24.04

# Set environment variables to avoid writing .pyc files and ensure stdout/stderr is flushed
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Accept build arguments for dynamic configuration of IP and Port
ARG NODE_IP=127.0.0.1
ARG NODE_PORT=6001
ARG NODE_COUNT=4

# Set environment variables from build arguments
ENV NODE_IP=${NODE_IP} \
    NODE_PORT=${NODE_PORT} \
    NODE_COUNT=${NODE_COUNT}

# Install necessary packages and dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-dev libgmp3-dev wget unzip cmake build-essential && \
    rm -rf /var/lib/apt/lists/*

# Download and install mcl
RUN wget https://github.com/herumi/mcl/archive/refs/tags/v1.93.zip && \
    unzip v1.93.zip && \
    cd mcl-1.93 && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make && \
    make install && \
    cd ../.. && \
    rm -rf mcl-1.93 v1.93.zip

# Create and set the working directory
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt /app/

# Install the Python dependencies
RUN pip3 install --break-system-packages -r requirements.txt

# Copy the required project files to the working directory
COPY node /app/zsequencer/node
COPY sequencer /app/zsequencer/sequencer
COPY common /app/zsequencer/common
COPY config.py /app/zsequencer/config.py
COPY run.py /app/zsequencer/run.py
COPY nodes.py /app/zsequencer/nodes.py

# Command to run the nodes.py script first and then run.py
CMD ["sh", "-c", "python3 zsequencer/nodes.py $NODE_IP $NODE_PORT && python3 zsequencer/run.py"]

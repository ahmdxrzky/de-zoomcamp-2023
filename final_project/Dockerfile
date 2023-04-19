# Use Python:3.8 as base image
FROM python:3.8

# Install nano and sudo
RUN apt-get update && \
    apt-get install -y nano sudo && \
    rm -rf /var/lib/apt/lists/*

# Copy files from local to container
COPY ./requirements.txt /app/requirements.txt
COPY ./src/data_pipeline.py /app/src/data_pipeline.py
RUN mkdir -p /app/config

# Set working directory
WORKDIR /app

# Install all of dependency packages
RUN pip install -r /app/requirements.txt

# Use bash as the entrypoint of container
ENTRYPOINT [ "bash" ]

# Use Python:3.8 as base image
FROM python:3.8

# Install nano and sudo
RUN apt-get update && \
    apt-get install -y nano sudo && \
    rm -rf /var/lib/apt/lists/*

# Install Terraform
ENV TERRAFORM_VERSION=1.1.0
RUN wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
    && unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
    && mv terraform /usr/local/bin \
    && rm terraform_${TERRAFORM_VERSION}_linux_amd64.zip

# Copy files from local to container
COPY ./requirements.txt /app/requirements.txt
COPY ./src/data_pipeline.py /app/src/data_pipeline.py
COPY ./src/manipulation_project_id.py /app/src/manipulation_project_id.py
COPY ./terraform/main.tf /app/terraform/main.tf
COPY ./terraform/variables.tf /app/terraform/variables.tf
RUN mkdir -p /app/config

# Set working directory
WORKDIR /app

# Install all of dependency packages
RUN pip install -r /app/requirements.txt

# Use bash as the entrypoint of container
ENTRYPOINT [ "bash" ]

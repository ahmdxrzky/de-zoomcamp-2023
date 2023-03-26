# Use Python:3.8 as base image
FROM python:3.8

# Install Terraform
ENV TERRAFORM_VERSION=1.1.0
RUN wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
    && unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
    && mv terraform /usr/local/bin \
    && rm terraform_${TERRAFORM_VERSION}_linux_amd64.zip

# Copy static files (files that doesn't need any adjustment) from local to container
COPY ./requirements.txt /app/requirements.txt
COPY ./final/data_pipeline.py /app/final/data_pipeline.py
COPY ./terraform/main.tf /app/terraform/main.tf

# Copy dynamic files from local to container
# Make sure "default" value for "project" and "credentials" variables has been changed
COPY ./terraform/variables.tf /app/terraform/variables.tf
# Change <path-to-service-account-keyfile> with folder structure for service account keyfile
# and change service-account-keyfile-name> with name of service account keyfile
COPY ./<path-to-service-account-keyfile>/<service-account-keyfile-name>.json /app/config/<service-account-keyfile-name>.json

# Set working directory
WORKDIR /app

# Install all of dependency packages
RUN pip install -r /app/requirements.txt

# Build infrastructure with terraform
RUN cd /app/terraform \
    && terraform init \
    && terraform plan \
    && terraform apply -auto-approve

# Use bash as the entrypoint of container
ENTRYPOINT [ "bash" ]

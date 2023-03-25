FROM python:3.8

# Install Terraform
ENV TERRAFORM_VERSION=1.1.0
RUN wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
    && unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
    && mv terraform /usr/local/bin \
    && rm terraform_${TERRAFORM_VERSION}_linux_amd64.zip

# Copy files from local to container
COPY ./terraform/main.tf /app/terraform/main.tf
COPY ./terraform/variables.tf /app/terraform/variables.tf
COPY ./assets /app/assets
COPY ./config/de-zoomcamp-375916-7d3bc8537cc2.json /app/config/de-zoomcamp-375916-7d3bc8537cc2.json
COPY ./requirements.txt /app/requirements.txt
COPY ./final/ingest_dataset.py /app/final/ingest_dataset.py
COPY ./final/extract_dataset.py /app/final/extract_dataset.py

# Set working directory
WORKDIR /app

# Install dependency packages
RUN pip install -r /app/requirements.txt

# # Build infrastructure with terraform
RUN cd /app/terraform \
    && terraform init \
    && terraform plan \
    && terraform apply -auto-approve

# Use bash as the entrypoint of container
ENTRYPOINT [ "bash" ]
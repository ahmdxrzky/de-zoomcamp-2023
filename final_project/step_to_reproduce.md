# Problem Statement
Patterns of weather are getting more difficult to be identified year by year. There are many factors that causing this, especially global warming. In the past, Indonesian people could be certain that the dry season would occur from this month to that month and the rainy on the other hand. Now, this is no longer the case. Therefore, this project aims to investigate the seasonal patterns in Denpasar City from 2011 to the present. <br>
Data source: Kaggle, Denpasar Weather Data

# Project Framework
![assets](https://user-images.githubusercontent.com/99194827/227752387-4736cd2d-ecf3-4579-a40e-1558f48d6413.png)
1. Pipeline for processing dataset and extracting it from source to a data lake.
2. Pipeline for batch moving the data from the data lake to a data warehouse.
3. Transform the data in the data warehouse.
4. Create a dashboard to see pattern of weather by year.

# Tools
### Cloud
![assets_cloud](https://user-images.githubusercontent.com/99194827/227749263-755e2813-5c6e-4c10-93d7-4a2b32515922.png)
- Google Compute Engine (GCE). A GCE virtual machine used to develop and run this project along with Google Cloud Storage (GCS) and Google BigQuery (GBQ).
- Terraform. Infrastructure as Code (IaC) tool to create a GCS Bucket and GBQ Dataset.
### Data Ingestion
![assets_ingestion](https://user-images.githubusercontent.com/99194827/227752393-db2c208e-8de5-40cb-bcf1-14c1dd8750b2.png)
- Prefect. Workflow Orchestration tool to orchestrarize data pipeline.
- Google Cloud Storage (GCS). GCS as Data Lake.
### Data Warehouse
![assets_warehouse](https://user-images.githubusercontent.com/99194827/227752398-cfe9a2c7-d9ca-4c5c-aa71-e47548758bf2.png) <br>
Google BigQuery (GBQ). GBQ as Data Warehouse. Table being partitioned by datetime.
### Data Transformations
![assets_transform](https://user-images.githubusercontent.com/99194827/227749726-b8a42fab-b1d3-4edf-80c3-c1cf4d7d10a7.png) <br>
data build tools (dbt). Tool for transforming data in data warehouse.
### Dashboard
![assets_dashboard](https://user-images.githubusercontent.com/99194827/227749757-ba2583de-a0b9-4815-bb6b-da7b5f62722a.png) <br>
Google Looker Studio. Tool for visualizing data in two tiles (for this project).

# Steps to Reproduce this Project
### Create Service Account
- Access Google Cloud Console. Then, move to "Service Accounts" tab.
  ![WhatsApp Image 2023-03-26 at 16 53 08](https://user-images.githubusercontent.com/99194827/227768394-016caefa-2b2f-42cb-b046-6c4c4f92660b.jpeg)
- Click "Create Service Account". Adjust some configuration, such as name and description, then click "Create". Grant all access needed by this service account to the project. Then, click "Done".
  ![WhatsApp Image 2023-03-26 at 16 53 08 (1)](https://user-images.githubusercontent.com/99194827/227768428-4fefee09-67ab-4b74-8774-7bd53a2216b4.jpeg) <br>
  ![WhatsApp Image 2023-03-26 at 16 53 08 (2)](https://user-images.githubusercontent.com/99194827/227768468-fb50c2e6-fdd6-4cc3-9ea7-ac510fb64ecc.jpeg) <br>
  ![WhatsApp Image 2023-03-26 at 16 53 08 (3)](https://user-images.githubusercontent.com/99194827/227768473-335ff2c5-8103-4e78-91cc-bba259f692a4.jpeg) <br>
- Click three dots on row of the newly built Service Account and click "Manage keys".
  ![WhatsApp Image 2023-03-26 at 16 53 08 (4)](https://user-images.githubusercontent.com/99194827/227768483-fef0ea5b-daa5-4eda-8f19-5b4187fb76a2.jpeg)
- Click "Add key" and "Create new key". Choose "json" option and a keyfile in json format will be downloaded automatically.
  ![WhatsApp Image 2023-03-26 at 16 53 08 (5)](https://user-images.githubusercontent.com/99194827/227768498-1a5a398b-7aee-47ea-aa9e-80b0b21caeb1.jpeg)
  ![WhatsApp Image 2023-03-26 at 16 53 09](https://user-images.githubusercontent.com/99194827/227768506-46f870b6-2b23-482b-b1a4-d8358206bb4b.jpeg)

### Create a Virtual Machine Instance on Google Compute Engine
- Access Google Cloud Console. Then, move to "VM Instances" tab.
  ![WhatsApp Image 2023-03-26 at 17 37 15](https://user-images.githubusercontent.com/99194827/227770469-dd40c2b8-4626-45ef-b34f-e7f704c52004.jpeg)
- Click "Create Instance". Adjust some configuration, such as name, region, and zone. In Firewall part, allow HTTP and HTTPS traffic. In Network part, define a network tags and enable IP forwarding. Then, click "Create".
  ![WhatsApp Image 2023-03-26 at 17 37 16](https://user-images.githubusercontent.com/99194827/227770476-4e7faf79-4c28-4b89-af89-e0b9029b2788.jpeg)
  ![WhatsApp Image 2023-03-26 at 17 37 20](https://user-images.githubusercontent.com/99194827/227770493-52efb4da-f336-4c0d-a367-01471b8bdb0b.jpeg)
  ![WhatsApp Image 2023-03-26 at 17 37 23](https://user-images.githubusercontent.com/99194827/227770499-370718e7-c557-4918-95ea-d14f74b7f91a.jpeg)
  ![WhatsApp Image 2023-03-26 at 17 37 27](https://user-images.githubusercontent.com/99194827/227770505-2f1f8f75-931e-4add-b7e4-521dd3e3fbc1.jpeg)
  Copy value from "External IP" column and use this to access VM from local terminal.
- Move to "Firewall" tab. Then, click "Create Firewall Rule"
  ![WhatsApp Image 2023-03-26 at 17 37 30](https://user-images.githubusercontent.com/99194827/227770509-0be648a5-dfb5-4e71-a653-4d78029d0c4f.jpeg)
  ![WhatsApp Image 2023-03-26 at 17 37 33](https://user-images.githubusercontent.com/99194827/227770527-2dc401bb-9958-40e5-a25d-e9f28ef76891.jpeg)
- Adjust name and description of firewall rule. Add "project" on target tags, "0.0.0.0/0" on Source IPv4 ranges, and 4200 on TCP ports. Then, click "Create".
  ![WhatsApp Image 2023-03-26 at 17 37 37](https://user-images.githubusercontent.com/99194827/227770534-5b7998d5-7d76-404a-ab27-6aeeb3ffd01b.jpeg)
  ![WhatsApp Image 2023-03-26 at 17 37 40](https://user-images.githubusercontent.com/99194827/227770541-cdf124a0-4728-4a57-a22d-239d851ae5e8.jpeg)
- Generate SSH Keygen
  ```bash
  ssh-keygen
  ```
  ![WhatsApp Image 2023-03-26 at 17 37 43](https://user-images.githubusercontent.com/99194827/227770547-b7050121-6b66-4cde-b28a-90ec859ea29b.jpeg)
- Copy output of RSA key below.
  ```bash
  cat ~/.ssh/id_rsa.pub
  ```
  ![WhatsApp Image 2023-03-26 at 17 37 47](https://user-images.githubusercontent.com/99194827/227770563-cbce5d86-bc61-447b-9b88-c977d9f685f7.jpeg)
- Paste RSA key to VM Instance. Click VM instance on Cloud Console "VM Instance" tab. Click "Edit". On "SSH Keys" part, click "Add item" and paste RSA key.
  ![WhatsApp Image 2023-03-26 at 17 37 50](https://user-images.githubusercontent.com/99194827/227770573-12134023-2f78-4531-8db0-3ddf9658d012.jpeg)
  ![WhatsApp Image 2023-03-26 at 17 37 54](https://user-images.githubusercontent.com/99194827/227770586-71064af8-cc39-4090-aed0-69531d74aec4.jpeg)
- VM can be accessed through local terminal-cli now.
  ```bash
  ssh <username>@<external-ip>
  ```
  Replace <username> with username on last part of RSA key and <external-ip> with value of external IP address of VM instance. Enter "yes". <br>
  ![WhatsApp Image 2023-03-26 at 17 37 56](https://user-images.githubusercontent.com/99194827/227770593-9fc2d3e4-fdbe-466a-9fa8-230266316ce9.jpeg)

### Clone Github Repository to Virtual Machine
- Install git on virtual machine.
  ```bash
  sudo apt-get install git
  ```
- In virtual machine terminal, clone this [github repository](https://github.com/ahmdxrzky/de-zoomcamp-2023).
  ```bash
  git clone https://github.com/ahmdxrzky/de-zoomcamp-2023.git && cd de-zoomcamp-2023/final_project
  ```
- Copy contents of keyfile previously downloaded to replace content in the config/example.json file.
  ![WhatsApp Image 2023-03-26 at 18 01 49](https://user-images.githubusercontent.com/99194827/227771446-97487d79-2632-4040-a5b2-c3c606353b9d.jpeg)
- Edit variables.tf on terraform folder. Change default "project" to personal project id.
  Before: <br>
  ![image](https://user-images.githubusercontent.com/99194827/227755227-0f915c22-4de4-4a10-9224-9d251e3d03fd.png) <br>
  After: <br>
  ![Screenshot 2023-03-26 112106](https://user-images.githubusercontent.com/99194827/227755721-f14ff9ac-f898-401e-8c6c-d891c8e586ac.png) <br>
  Personal project id can be seen in cloud console: <br>
  ![Screenshot 2023-03-26 112329](https://user-images.githubusercontent.com/99194827/227755302-2ec9f3e1-3b6c-4175-a003-0ed092bf8b87.png)
  
### Deploy Docker Image
- Install docker
  ```bash
  sudo apt-get install docker.io
  ls -l /var/run/docker.sock
  sudo chmod 666 /var/run/docker.sock
  ```
- Build docker image based on Dockerfile
  ```bash
  docker build -t rizky_dezoomcamp_final_project ./
  ```
- Run docker container based on previously built docker image also exposing port 4200 for Prefect UI.
  ```bash
  docker run -p 4200:4200 -it rizky_dezoomcamp_final_project
  ```

## Do Configuration on Prefect
- Activate Prefect
  ```bash
  prefect server start --host 0.0.0.0
  ```
- Create Prefect Block for GCP Credentials
  docker ps -a
  docker exec -it <container-id> /bin/bash
  ```bash
  prefect config set PREFECT_API_URL=http://0.0.0.0:4200/api
  prefect block create gcp-credentials
  ```
  Click link provided from command above. Fill `gcp-credentials-final-project` for the block on `Block Name` and `/app/config/<key-file-name>.json` on `Service Account File`. Then, click `Create`.
- Create Prefect Block for GCS Bucket
  ```bash
  prefect block create gcs-bucket
  ```
  Click link provided from command above. Fill `gcs-bucket-final-project` for the block on `Block Name`, `dezoomcamp_final_project` on `Bucket`, and choose which GCP Credentials embedded with the bucket on `Gcp Credentials`. Then, click `Create`.

## Ingest Initial Dataset
In this project, we simulate to do batch processing from data lake to data warehouse. Therefore, we should first define making sure that there are all data needed in data lake. To do this, we do ETL process using Prefect from source on internet into Google Cloud Storage by executing command below:
```bash
python3 final/data_pipeline.py True
```
By executing command above, we make sure weather data of Denpasar City from Jan 2011 to Dec 2023 are already on GCS. Why data from 2023 are already available to December? Surely, this data is imitative. I make it like that to stimulate real batch processing done monthly.<br>
Now, we'll ingest data from Jan 2011 to Jan 2023 only to Google BigQuery, because the rest of it will be ingested batch per month. It can be done by executing command below:
```bash
python3 final/data_pipeline.py
```
Using Prefect Deployment, data of Feb 2023 will be ingested in March 1st, 2023 and data of Mar 2023 will be ingested in Apr 1st, 2023, etc.

## Create, Apply, and Run Prefect Deployment for Monthly Batch Processing
To ingesting dataset batch per month, we create and apply Prefect Deployment and set the cron to run monthly, by executing command below:
```bash
prefect deployment build /app/final/extract_dataset.py:etl_monthly -n "ETL GCS to BGQ Monthly" --cron "0 0 1 * *" -a
```
Don't forget to start a Prefect Agent for the deployment by executing command below:
```bash
prefect agent start -q 'default'
```
This deployment will run batch processing of previous month at 1st date of current month.

## Data Transformation on Data Warehouse with dbt Cloud
Register or Sign in
Account settings > Add project > Connect github repo (connect with Github account and select repository) and bigquery connection (upload service account key file)
Profile settings > Credentials > Select project > Development credentials > Dataset final_project
Go to `Develop` tab, then commit and push that to development branch on remote repository.
dbt seed
dbt run

## Looker studio
Add data source

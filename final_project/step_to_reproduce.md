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
- Move to "Service Account" tab. <br>
  ![Screenshot 2023-03-26 102244](https://user-images.githubusercontent.com/99194827/227753469-b87d19bd-d470-4945-98b5-83ef6ad79fde.png)
- Click "Create a Service Account". Adjust some configuration, such as name, id, and description, then click "Create". <br>
  ![Screenshot 2023-03-26 102443](https://user-images.githubusercontent.com/99194827/227753532-726fb56e-2f0c-43ef-a7d1-636dd39126bd.png)
- Click three dots on row of the newly built Service Account and click "Manage keys". <br>
  ![Screenshot 2023-03-26 102844](https://user-images.githubusercontent.com/99194827/227753695-35fbf26c-0a9a-459f-98e3-431a7f74b951.png)
- Click "Add key" and "Create new key". Choose "json" option and a keyfile in json format will be saved automatically.

### Create a Virtual Machine Instance on Google Compute Engine
- Login to Google Cloud Console and move to "Compute Engine" tab. <br>
  ![Screenshot 2023-03-26 101813](https://user-images.githubusercontent.com/99194827/227753342-fff3ae4e-eb86-4ca7-a573-5fa36c92b013.png)
- Click "Create Instance". Adjust some configuration, such as name, region, and zone, then click "Create". <br>
  ![Screenshot 2023-03-26 101942](https://user-images.githubusercontent.com/99194827/227753416-1d511350-3e8d-4264-9aec-ba24a3d4c9c9.png)
- A VM Instance has been built, shown below: <br>
  ![Screenshot 2023-03-26 101051](https://user-images.githubusercontent.com/99194827/227753185-42176bad-8f7e-461d-a2bf-d045925d1622.png)
- Access our virtual machine by clicking "SSH" next to "External IP" column.

### Clone Github Repository to Virtual Machine
- Install git on virtual machine.
  ```bash
  sudo apt-get install git
  ```
- In virtual machine terminal, clone this [github repository](https://github.com/ahmdxrzky/de-zoomcamp-2023).
  ```bash
  git clone https://github.com/ahmdxrzky/de-zoomcamp-2023.git
  mv de-zoomcamp-2023/final_project/ ./ && rm -rf de-zoomcamp-2023/
  ```
- Copy contents of keyfile previously downloaded to the config/example.json file.
- Edit variables.tf on terraform folder. Change default "project" to personal project id. <br>
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

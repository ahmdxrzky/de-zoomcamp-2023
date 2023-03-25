# Introduction
Patterns of weather are getting more difficult to be identified year by year. There are many factors that causing this, especially global warming. In the past, Indonesian people could be certain that the dry season would occur from this month to that month and the rainy on the other hand. Now, this is no longer the case. Therefore, this project aims to investigate the seasonal patterns in Denpasar City from 2011 to the present.
Data source: Kaggle, Denpasar Weather Data

# Solution
1. Create a pipeline for processing dataset and putting it to a data lake.
2. Create a pipeline for batch moving the data from the data lake to a data warehouse.
3. Transform the data in the data warehouse.
4. Create a dashboard to see pattern of weather by year.

# Steps to Reproduce this Project

## Create Service Account
Create a Service Account for Google Cloud Platform. Create a key for that Service Account. Download that key file (in json format).

Put Key file to config folder
Edit variables.tf on terraform folder. default project and credentials adjusting with self

## Deploy Docker Image
docker build -t rizky_dezoomcamp_final_project ./
docker run -p 4200:4200 -it rizky_dezoomcamp_final_project

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
python3 final/ingest_dataset.py
```
By executing command above, we make sure weather data of Denpasar City from Jan 2011 to Dec 2023 are already on GCS. Why data from 2023 are already available to December? Surely, this data is imitative. I make it like that to stimulate real batch processing done monthly.<br>
Now, we'll ingest data from Jan 2011 to Jan 2023 only to Google BigQuery, because the rest of it will be ingested batch per month. It can be done by executing command below:
```bash
python3 final/extract_dataset.py True
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

# Introduction
Patterns of weather are becoming more difficult to be identified year by year. There are many factors that causing this, especially global warming. In the past, Indonesian people could be certain that the dry season would occur from this month to that month and the rainy on the other hand. Now, this is no longer the case. Therefore, this project aims to investigate the seasonal patterns in Denpasar City from 2011 to the present.
Data source: Kaggle, Denpasar Weather Data

# Solution
1. Create a pipeline for processing dataset and putting it to a data lake.
2. Create a pipeline for batch moving the data from the data lake to a data warehouse.
3. Transform the data in the data warehouse.
4. Create a dashboard to see pattern of weather by year.

# Steps to Reproduce this Project

## Deploy Docker Image
In this project, we need some softwares and folders, stated as follows:
1. `requirements.txt`: (file) list of dependable python packages
2. `Terraform`: (software) platform of Infrastructure as a Code
3. `terraform`: (folders) files for terraform configuration
Those softwares can be easily downloaded by composing [this Dockerfile]() up.<br>

## Create Service Account
Create a Service Account for Google Cloud Platform. Create a key for that Service Account. Download that key file (in json format).

## Build the Infrastructures
In this project, we need Google Cloud Storage (GCS) as Data Lake and Google BigQuery (GBQ) as Data Warehouse. Those infrastructures can be built in a time using Terraform.<br>
Access `terraform` folder with terminal and execute these command:
```bash
terraform init
terraform plan
terraform apply
```
When executing `terraform plan` and `terraform apply`, terminal will ask value for `project` and `credentials` variable.<br>
Open service account key file and see value for "project_id" key. Use this value for `project` variable.<br>
Copy path of the service account key file. Use this value for `credentials` variable.<br>
After this process, a GCS bucket and a GBQ dataset have been built.

## Do Configuration on Prefect
- Activate Prefect
  ```bash
  prefect orion start
  ```
- Create Prefect Block for GCP Credentials
  ```bash
  prefect block create gcp-credentials
  ```
  Click link provided from command above. Fill name for the block on `Block Name` and paste path of service account key file on `Service Account File`. Then, click `Create`.
- Create Prefect Block for GCS Bucket
  ```bash
  prefect block create gcs-bucket
  ```
  Click link provided from command above. Fill name for the block on `Block Name`, name of the bucket built from terraform previously on `Bucket`, and choose which GCP Credentials embedded with the bucket on `Gcp Credentials`. Then, click `Create`.

## Ingest Initial Dataset
In this project, we simulate to do batch processing from data lake to data warehouse. Therefore, we should first define making sure that there are all data needed in data lake. To do this, we do ETL process using Prefect from source on internet into Google Cloud Storage by executing command below:
```bash
python3 ingest_dataset.py
```
By executing command above, we make sure weather data of Denpasar City from Jan 2011 to Dec 2023 are already on GCS. Why data from 2023 are already available to December? Surely, this data is imitative. I make it like that to stimulate real batch processing done monthly.<br>
Now, we'll ingest data from Jan 2011 to Jan 2023 only to Google BigQuery, because the rest of it will be ingested batch per month. It can be done by executing command below:
```bash
python3 extract_dataset.py True
```
Using Prefect Deployment, data of Feb 2023 will be ingested in March 1st, 2023 and data of Mar 2023 will be ingested in Apr 1st, 2023, etc.

## Create, Apply, and Run Prefect Deployment for Monthly Batch Processing
To ingesting dataset batch per month, we create and apply Prefect Deployment and set the cron to run monthly, by executing command below:
```bash
prefect deployment build ./extract_dataset.py:etl_monthly -n "ETL GCS to BGQ Monthly" --cron "0 0 1 * *" -a
```
Don't forget to start a Prefect Agent for the deployment by executing command below:
```bash
prefect agent start -q 'default-agent-pool
```
This deployment will run batch processing of previous month at 1st date of current month.

## Data Transformation on Data Warehouse with dbt Cloud
Connect a github repository and bigquery connection to dbt Cloud. Remember to create a development branch on the repository.<br>
Go to `Develop` tab and click `Initialize`, then commit and push that to development branch on remote repository.<br>
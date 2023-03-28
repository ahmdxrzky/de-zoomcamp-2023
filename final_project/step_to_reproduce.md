# Problem Statement
Patterns of weather are getting more difficult to be identified year by year. There are many factors that causing this, especially global warming. In the past, Indonesian people could be certain that the dry season would occur from this month to that month and the rainy on the other hand. Now, this is no longer the case. Therefore, this project aims to investigate the seasonal patterns in Denpasar City from 2011 to the present. <br>
Data source: Kaggle, Denpasar Weather Data

# Project Framework
![assets](https://user-images.githubusercontent.com/99194827/227752387-4736cd2d-ecf3-4579-a40e-1558f48d6413.png)
1. Pipeline for processing dataset and extracting it from source to a data lake.
2. Pipeline for batch moving the data from the data lake to a data warehouse.
3. Transform the data in the data warehouse.
4. Create a dashboard to see pattern of weather by year. <br>

This project's guidance assumed readers have already know basic syntax for linux administration, such as `nano` to edit file on linux or `cat` to see content from a file in linux terminal.

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
## Create Service Account
### Access Google Cloud Console [here](https://console.cloud.google.com/getting-started). Then, move to "Service Accounts" tab.
![Cloud Console](https://user-images.githubusercontent.com/99194827/228078545-add2b3b8-202d-4ffd-989f-0122b5969980.png)
### Click "Create Service Account".
![Screenshot 2023-03-28 051305](https://user-images.githubusercontent.com/99194827/228079307-30829881-8e52-44d0-8aed-39f20d25f849.png)
### Fill in name and description (ID is auto-generate based on name) for service account, then click "Create".
![Screenshot 2023-03-28 051359](https://user-images.githubusercontent.com/99194827/228079334-9bd09e3c-ab51-400a-ace9-cbeffbfc1592.png)
### Grant all access needed by this service account to the project. Since this project will work around Cloud Storage and BigQuery, so I grant these roles for this service account. Then, click "Continue". Then, click "Done" on bottom of the page.
![Screenshot 2023-03-28 051754](https://user-images.githubusercontent.com/99194827/228079475-2a304a14-01ae-4646-ab5f-b710d20203a9.png)
### Click three dots on row of the newly built Service Account and click "Manage keys".
![Screenshot 2023-03-28 052039](https://user-images.githubusercontent.com/99194827/228079986-950b8695-1e61-4fd0-8d1e-20476df5b441.png)
### Click "Add key" and "Create new key".
![Screenshot 2023-03-28 052151](https://user-images.githubusercontent.com/99194827/228080151-dd07124c-5182-46d1-9d7e-2d4ddc656426.png)
### Choose "JSON" option and a keyfile in json format will be downloaded automatically. Save this for later.
![Screenshot 2023-03-28 052232](https://user-images.githubusercontent.com/99194827/228080289-f73e2675-3bf9-44f3-b6a1-dd6a812852cf.png)

## Create a Virtual Machine Instance on Google Compute Engine
### Still in Google Cloud Console, move to "VM Instances" tab.
![Screenshot 2023-03-28 052449](https://user-images.githubusercontent.com/99194827/228080597-900e3bb8-96b9-4e12-b1b4-f81a03683aa3.png)
### Click "Create Instance".
![Screenshot 2023-03-28 052531](https://user-images.githubusercontent.com/99194827/228080697-2cf00073-8e38-48c3-a1ff-012784f3a330.png)
### Fill in name, region, and zone.
![Screenshot 2023-03-28 052637](https://user-images.githubusercontent.com/99194827/228080851-981302b9-4a28-49fe-8839-6d1463c60b37.png)
### Scroll down. In Firewall part, allow HTTP and HTTPS traffic.
![Screenshot 2023-03-28 052723](https://user-images.githubusercontent.com/99194827/228081008-64cd7a46-d291-4eb5-839e-11c373d19493.png)
### Scroll down again and drop down "Advanced options". In Networking part, fill in network tags and enable IP forwarding. Then, click "Create" on bottom of the page.
![Screenshot 2023-03-28 052913](https://user-images.githubusercontent.com/99194827/228081268-5154c229-14d0-47e1-bf8c-826f2aaba207.png)
### Remember value from "External IP" column. It will be used for accessing this VM from local machine.
![Screenshot 2023-03-28 053032](https://user-images.githubusercontent.com/99194827/228081528-30053ed9-8a82-48d6-b9e1-ec2cf55b1f86.png)
### Move to "Firewall" tab. Then, click "Create Firewall Rule"
![Screenshot 2023-03-28 053143](https://user-images.githubusercontent.com/99194827/228081668-97d46b2e-6e3c-43a7-8aa3-ff07643cf54a.png)
![Screenshot 2023-03-28 053232](https://user-images.githubusercontent.com/99194827/228085307-0d8c1bac-d9fa-4545-8509-824f9957472e.png)
### Adjust name and description of firewall rule.
![Screenshot 2023-03-28 053336](https://user-images.githubusercontent.com/99194827/228081917-55e32bf8-7662-4a80-9360-236cf464dcb9.png)
### Fill in "project" on target tags (so this rule will apply to all VM with this tag, including the newly built one), "0.0.0.0/0" on Source IPv4 ranges (so all external machine can access this VM), and 4200 on TCP ports (port for Prefect UI). Then, click "Create" on bottom of the page.
![Screenshot 2023-03-28 053556](https://user-images.githubusercontent.com/99194827/228082396-ce6819db-415a-42bb-bc11-6997f2ca55e8.png)
### Move to local terminal (I use wsl terminal on Visual Studio Code. This also can be done with command prompt for windows). Then, generate SSH Keygen.
```bash
ssh-keygen
```
### Copy output of this command.
```bash
cat ~/.ssh/id_rsa.pub
```
### Click previously built VM instance.
![Screenshot 2023-03-28 054131](https://user-images.githubusercontent.com/99194827/228083451-edcf0d0f-57e4-4821-9252-c469a4266e49.png)
### Click "Edit".
![Screenshot 2023-03-28 054144](https://user-images.githubusercontent.com/99194827/228083508-78e27ad8-fe32-4a97-9a21-f43123c13447.png)
### On "SSH Keys" part, click "Add item" and paste RSA key from local terminal copied before. Then, click "Save" on bottom of the page.
Before: <br>
![Screenshot 2023-03-28 054214](https://user-images.githubusercontent.com/99194827/228083563-630142b0-6277-47fd-83d7-084ac24d699e.png) <br>
After: <br>
![Screenshot 2023-03-28 054235](https://user-images.githubusercontent.com/99194827/228083588-598ead42-e167-4309-a80c-981893591987.png)
### VM can be accessed through local terminal-cli now.
```bash
ssh <username>@<external-ip>
```
Replace `<username>` with username of wsl machine and `<external-ip>` with value of external IP address of VM instance.
![Screenshot 2023-03-28 054703](https://user-images.githubusercontent.com/99194827/228083970-62a10890-d508-4384-91d5-9756529ae59f.png)

## Clone Github Repository to Virtual Machine
### Install git on virtual machine.
```bash
sudo apt-get install git -y
```
### In virtual machine terminal, clone this [github repository](https://github.com/ahmdxrzky/de-zoomcamp-2023). Then, change working directory to final_project folder.
```bash
git clone https://github.com/ahmdxrzky/de-zoomcamp-2023.git && cd de-zoomcamp-2023/final_project
```
### Copy contents of keyfile previously downloaded to replace content in the config/keyfile.json file.
Before: <br>
![Screenshot 2023-03-28 060505](https://user-images.githubusercontent.com/99194827/228086611-ea35c539-5b90-4566-9807-29799240608c.png) <br>
After: <br>
![Screenshot 2023-03-28 060521](https://user-images.githubusercontent.com/99194827/228086639-eb88867c-22cb-4afa-8cd2-336c0d6ec04d.png)
### Edit variables.tf on terraform folder. Change default "project" to personal project id.
Before: <br>
![Screenshot 2023-03-28 060756](https://user-images.githubusercontent.com/99194827/228086951-05b40b94-1ade-4074-a072-c1e9174c0bb6.png) <br>
After: <br>
![Screenshot 2023-03-28 060905](https://user-images.githubusercontent.com/99194827/228086971-8687b1d2-7e64-4e93-b731-4ec493a2a0cc.png) <br>
Personal project id can be obtained from service account keyfile downloaded and copied before. <br>
![image](https://user-images.githubusercontent.com/99194827/228087061-9a8bdd2c-c733-403d-9e8c-f84b27ff2d08.png)
  
## Build Docker Image and Run Docker Container
### Install docker on virtual machine.
```bash
sudo apt-get install docker.io -y
sudo chmod 666 /var/run/docker.sock
```
### Still in final_project working directory, build docker image based on Dockerfile
```bash
docker build -t rizky_dezoomcamp_final_project ./
```
### Run docker container based on previously built docker image also exposing port 4200 for Prefect UI.
```bash
docker run -p 4200:4200 -it rizky_dezoomcamp_final_project
```

## Activate and Configurate Prefect
### Activate and Access Prefect UI.
```bash
prefect config set PREFECT_API_URL=http://<external-ip>:4200/api
prefect server start --host 0.0.0.0
```
Now, Prefect UI can be accessed from web browser with URL `<external-ip>:4200`. Replace `<external-ip>` with external IP address of the VM.
### Create Prefect Block for GCP Credentials
From Prefect UI, move to 'Blocks' tab.
![Screenshot 2023-03-28 062930](https://user-images.githubusercontent.com/99194827/228089527-687c69f4-3ba6-42f1-94c1-b5ad9d115cc3.png) <br>
Click "+" button, search "GCP Credentials", then click "+ Add". <br>
![Screenshot 2023-03-28 063111](https://user-images.githubusercontent.com/99194827/228089771-b5d2a243-7ecc-4f8a-b032-7a01bd335d23.png) <br>
Fill `gcp-credentials-final-project` for the block on `Block Name` and `/app/config/keyfile.json` on `Service Account File`. Then, click `Create`.
![image](https://user-images.githubusercontent.com/99194827/228089865-a8b74240-f14b-4504-92c9-69938e2f6d2c.png)
### Create Prefect Block for GCS Bucket
Move again to 'Blocks' tab. Click "+" button, search "GCS Bucket", then click "+ Add". <br>
![image](https://user-images.githubusercontent.com/99194827/228090032-a5a7d758-543b-4296-9404-411202c0398c.png) <br>
Fill `gcs-bucket-final-project` for the block on `Block Name`, `dezoomcamp_final_project` on `Bucket`, and choose which GCP Credentials embedded with the bucket on `Gcp Credentials`. Then, click `Create`. <br>
![image](https://user-images.githubusercontent.com/99194827/228090227-34a9c702-6468-4979-871d-12bea89a86f8.png)
### Open new terminal and access vm in the new terminal using ssh (same as before). Access same container by checking its id and run with exec command.
```bash
docker ps -a
docker exec -it <container-id> bash
```
Replace `<container-id>` with container id shown in output of command `docker ps -a`. <br>
![Screenshot 2023-03-28 062241](https://user-images.githubusercontent.com/99194827/228088746-9e988e0a-998a-484a-a7ee-d6558460ce58.png)

## Ingest Initial Dataset
In this project, we simulate to do batch processing from source to data lake to data warehouse. Now, we'll ingest data from Jan 2011 to Jan 2023 as initial state of dataset. It can be done by executing command below:
```bash
python3 final/initial_dataset.py True
```
Terminal's condition on prefect running: <br>
![image](https://user-images.githubusercontent.com/99194827/228159806-2600a11d-5324-4a8d-9c93-8a4634c86407.png) <br>
BigQuery's query when initial dataset has been ingested: <br>
![image](https://user-images.githubusercontent.com/99194827/228160232-18edf66c-72e7-44d1-8338-008f0c5ec1f3.png) <br>
Using Prefect Deployment, data of Feb 2023 will be ingested in March 1st, 2023 and data of Mar 2023 will be ingested in Apr 1st, 2023, etc.

## Create, Apply, and Run Prefect Deployment for Monthly Batch Processing
To ingest data per batch monthly, we create and apply Prefect Deployment and set the cron to run monthly, by executing command below:
```bash
prefect deployment build /app/final/data_pipeline.py:etl_total -n "ETL GCS to BGQ Monthly" --cron "0 0 1 * *" -a
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

# Problem Statement
Pattern of weather is getting more difficult to be identified year by year. Usually, Indonesian people could certain that the dry season would occur from March to September and the rainy season on the other hand. Now, we can no longer use this knowledge as reference. Therefore, I am interested to build this project in order to answer the question of _whether there have been changes in weather patterns in Denpasar or not_.

# Data Source
#### [_Denpasar Weather Data on Kaggle_](https://www.kaggle.com/datasets/cornflake15/denpasarbalihistoricalweatherdata?resource=download) ####
Disclaimer: Actually, dataset above only provides weather data of Denpasar City from 1990 to 2020 (even the data for 2020 is not complete to December). In order to make this data engineering project (which batch processes the data) looks real and simulate the actual workflow of data engineering, I _manipulate_ the dataset by _adding_ 4 years to the actual date data and _dividing_ it per year and month, so the data for 2023 are available and can be used to simulate batch processing per month. I put this splitted data [here](https://github.com/ahmdxrzky/de-zoomcamp-2023/tree/main/final_project/assets/dataset).

# Project Framework
![assets drawio](https://user-images.githubusercontent.com/99194827/229009417-e04e2add-29fa-45e3-aa8f-cf094ca23df9.png)
1. Pipeline for processing dataset and extracting it from source to a data lake.
2. Pipeline for batch moving the data from the data lake to a data warehouse.
3. Transform the data in the data warehouse.
4. Create a dashboard to see pattern of weather by year.

# Tools
### Cloud
- **Google Compute Engine (GCE)**. A GCE virtual machine used to develop and run this project along with Google Cloud Storage (GCS) and Google BigQuery (GBQ).
- **Terraform**. Infrastructure as Code (IaC) tool to create a GCE VM Instance, GCS Bucket and GBQ Dataset in a code execution only.
- **Docker** and **Docker Hub**. Tool for containerizing environment of this data pipeline project.
### Data Ingestion
- **Prefect**. Workflow Orchestration tool to orchestrarize data pipeline.
- **Google Cloud Storage (GCS)**. GCS as Data Lake.
### Data Warehouse
- **Google BigQuery (GBQ)**. GBQ as Data Warehouse. Table being partitioned by datetime.
### Data Transformations
- **data build tools (dbt)**. Tool for transforming data in data warehouse.
### Dashboard
- **Google Looker Studio**. Tool for visualizing data in two tiles (for this project).

# Steps to Reproduce this Project
### Create Service Account
- Access **Google Cloud Console** [here](https://console.cloud.google.com/getting-started). Login with your google account. Then, move to **Service Accounts** tab. (You have to select a cloud project or create one if you didn't have any)
  ![Cloud Console](https://user-images.githubusercontent.com/99194827/228078545-add2b3b8-202d-4ffd-989f-0122b5969980.png)
- Click **Create Service Account**.
  ![Screenshot 2023-03-28 051305](https://user-images.githubusercontent.com/99194827/228079307-30829881-8e52-44d0-8aed-39f20d25f849.png)
- Fill in name and description (ID is auto-generate based on name) for service account, then click **Create and Continue**.
  ![Screenshot 2023-03-28 051359](https://user-images.githubusercontent.com/99194827/228079334-9bd09e3c-ab51-400a-ace9-cbeffbfc1592.png)
- Grant all access needed by this service account to the project. I grant these roles for this service account. Then, click **Continue**. Then, click **Done** on bottom of the page.
  ![image](https://user-images.githubusercontent.com/99194827/233023621-5458c1c4-3a83-4dbc-b5a2-1cc45ae6247e.png)
- Click three dots on row of the newly built Service Account and click **Manage keys**.
  ![Screenshot 2023-03-28 052039](https://user-images.githubusercontent.com/99194827/228079986-950b8695-1e61-4fd0-8d1e-20476df5b441.png)
- Drop **Add key** down, then click **Create new key**.
  ![Screenshot 2023-03-28 052151](https://user-images.githubusercontent.com/99194827/228080151-dd07124c-5182-46d1-9d7e-2d4ddc656426.png)
- Choose **JSON** option, then click **Create**. A keyfile in json format will be downloaded automatically.
  ![Screenshot 2023-03-28 052232](https://user-images.githubusercontent.com/99194827/228080289-f73e2675-3bf9-44f3-b6a1-dd6a812852cf.png)

### Build GCE VM Instance, GCS Bucket, GBQ Dataset, and Firewall Rule with Terraform
- Clone this repository to your host machine and move to  by executing this command.
  ```bash
  git clone https://github.com/ahmdxrzky/de-zoomcamp-2023.git
  cd de-zoomcamp-2023/final_project/terraform
  ```
- Install Terraform by executing this command.
  ```bash
  wget https://releases.hashicorp.com/terraform/1.4.0/terraform_1.4.0_linux_amd64.zip \
    && unzip terraform_1.4.0_linux_amd64.zip \
    && sudo mv terraform /usr/local/bin \
    && rm terraform_1.4.0_linux_amd64.zip
  ```
- Insert project id to terraform/variables.tf file. <br>
  Open terraform/variables.tf by executing command below.
  ```
  nano variables.tf
  ```
  Personal project id can be seen in google cloud console.
  ![Screenshot 2023-03-29 093459](https://user-images.githubusercontent.com/99194827/228412084-a15023e3-2fe5-4823-ab0a-614b3a7caf3d.png)
  Replace `<gcp-project-id>` in terraform/variables.tf file with copied project id above.
- Copy content of keyfile json downloaded before. Execute this command below.
  ```bash
  mkdir -p ../config
  nano ../config/keyfile.json
  ```
  Then, paste content of keyfile json in here.
  ![Screenshot 2023-03-28 060521](https://user-images.githubusercontent.com/99194827/228086639-eb88867c-22cb-4afa-8cd2-336c0d6ec04d.png)
  Last, save the file.
- Build all infrastructure needed with Terraform by executing this command below.
  ```
  terraform init \
    && terraform plan \
    && terraform apply -auto-approve
  ```
  
  _LOGICAL FRAMEWORK_ <br>
  1. _**Terraform**, as Iac Tool, creates infrastructures by read these two files, [main.tf](https://github.com/ahmdxrzky/de-zoomcamp-2023/blob/main/final_project/terraform/main.tf) and [variables.tf](https://github.com/ahmdxrzky/de-zoomcamp-2023/blob/main/final_project/terraform/variables.tf)_
  2. _**variables.tf** file contains definition (name, description, default value, and data type) of variables that will be used in main.tf file. In this project, I created **resource_name**, **project**, **region**, **zone**, **credentials**, **storage_class**, and **BQ_DATASET** variables which contain value of name for VM Instance and GCS Bucket, personal project id, region and zone for resource, path to service account keyfile, storage class, and name for GBQ Dataset, respectively._
  3. _**main.tf** file contains codes to build GCE Instance, Firewall Rule, GCS Bucket, and GBQ Dataset based on variables on variables.tf file._
- Move to local terminal (I use wsl terminal on Visual Studio Code. This also can be done with command prompt for windows). Check have you generate a SSH key or not by executing this command.
  ```bash
  cat ~/.ssh/id_rsa.pub
  ```
  If there is no `id_rsa.pub` file on your machine, it means you haven't generate any SSH key. If there is output from the command above, you can skip this very next step.
- Generate SSH key by executing this command.
  ```bash
  ssh-keygen
  ```
- Read content of `id_rsa.pub` file and copy it.
- Back to **Google Cloud Console**. Go to **VM Instances** tab and click newly built VM instance.
  ![Screenshot 2023-03-28 054131](https://user-images.githubusercontent.com/99194827/228083451-edcf0d0f-57e4-4821-9252-c469a4266e49.png)
- Click **Edit**.
  ![Screenshot 2023-03-28 054144](https://user-images.githubusercontent.com/99194827/228083508-78e27ad8-fe32-4a97-9a21-f43123c13447.png)
- On **SSH Keys** part, click **+ Add item** and paste RSA key from local terminal copied on step 11. Then, click **Save** on bottom of the page. <br>
  Before: <br>
  ![Screenshot 2023-03-28 054214](https://user-images.githubusercontent.com/99194827/228083563-630142b0-6277-47fd-83d7-084ac24d699e.png) <br>
  After: <br>
  ![Screenshot 2023-03-28 054235](https://user-images.githubusercontent.com/99194827/228083588-598ead42-e167-4309-a80c-981893591987.png)
- VM can be accessed through local terminal-cli now.
  ```bash
  ssh <username>@<external-ip>
  ```
  Replace `<username>` with username of machine and `<external-ip>` with value of external IP address of VM instance.
  ![Screenshot 2023-04-01 105951](https://user-images.githubusercontent.com/99194827/229264688-5f51e356-03ce-44fa-b886-ea4ad4598896.png)

### Setup Environment with Docker
- Make sure you are already in terminal of VM. Docker has been installed when VM Instance being built.
- Environment for this data engineering pipeline has been created based on this [Dockerfile](https://github.com/ahmdxrzky/de-zoomcamp-2023/blob/main/final_project/Dockerfile) and pushed to Image Registry of Docker which is Docker Hub. I've set it publicly accessible, so everyone can create a container based on this Docker Image.
  ![image](https://user-images.githubusercontent.com/99194827/233032298-9d069671-c2d1-4975-86c6-cec49fa2b183.png) <br>
  Execute this command below to run docker container based on docker images above.
  ```bash
  docker run -p 4200:4200 -e EXTERNAL_IP=<external-ip> -it ahmdxrzky/dezoomcamp_final_project:0.0.5
  ```
  Change `<external-ip>` with external IP address of VM instance <br>
  ![Screenshot 2023-04-19 163226](https://user-images.githubusercontent.com/99194827/233033302-dd826597-d910-481f-8610-3402a4e1000b.png)

  _LOGICAL FRAMEWORK_ <br>
  _I build this docker image based on this [Dockerfile](https://github.com/ahmdxrzky/de-zoomcamp-2023/blob/main/final_project/Dockerfile) which use **Python:3.8** as base image. This image containerize:_
  1. _**Install** sudo and nano_
  2. _**Copy** [requirements.txt](https://github.com/ahmdxrzky/de-zoomcamp-2023/blob/main/final_project/requirements.txt) and [data_pipeline.py](https://github.com/ahmdxrzky/de-zoomcamp-2023/blob/main/final_project/src/data_pipeline.py)_
  3. _**Create** config folder_
  4. _**Use** /app folder as working directory_
  5. _**Install** dependency libraries for Python from requirements.txt_
  6. _**Use** bash as entrypoint._  
- Copy content of keyfile json downloaded before. Execute this command below.
  ```bash
  nano /app/config/keyfile.json
  ```
  Then, paste content of keyfile json in here.
  ![Screenshot 2023-03-28 060521](https://user-images.githubusercontent.com/99194827/228086639-eb88867c-22cb-4afa-8cd2-336c0d6ec04d.png)
  Last, save the file.

### Activate and Configurate Prefect
- Activate and Access Prefect UI.
  ```bash
  prefect config set PREFECT_API_URL=http://$EXTERNAL_IP:4200/api
  prefect server start --host 0.0.0.0
  ```
  Now, Prefect UI can be accessed from web browser with URL `<external-ip>:4200`.
  ![Screenshot 2023-04-01 105736](https://user-images.githubusercontent.com/99194827/229264603-4dd9bd7d-c097-4e31-9213-ca047d622a25.png)
- Create Prefect Block for GCP Credentials. <br>
  From Prefect UI, move to **Blocks** tab.
  ![Screenshot 2023-03-28 062930](https://user-images.githubusercontent.com/99194827/228089527-687c69f4-3ba6-42f1-94c1-b5ad9d115cc3.png) <br>
  Click **+** button, search **GCP Credentials**, then click **+ Add**. <br>
  ![Screenshot 2023-03-28 063111](https://user-images.githubusercontent.com/99194827/228089771-b5d2a243-7ecc-4f8a-b032-7a01bd335d23.png) <br>
  Fill `gcp-credentials-final-project` for the block on **Block Name** and `/app/config/keyfile.json` on **Service Account File**. Then, click **Create**.
  ![image](https://user-images.githubusercontent.com/99194827/228089865-a8b74240-f14b-4504-92c9-69938e2f6d2c.png)
- Create Prefect Block for GCS Bucket. <br>
  Move again to **Blocks** tab. Click **+** button, search **GCS Bucket**, then click **+ Add**. <br>
  ![image](https://user-images.githubusercontent.com/99194827/228090032-a5a7d758-543b-4296-9404-411202c0398c.png) <br>
  Fill `gcs-bucket-final-project` for the block on **Block Name**, `dezoomcamp-final-project` on **Bucket**, and choose which GCP Credentials embedded with the bucket on **Gcp Credentials**. Then, click **Create**. <br>
  ![image](https://user-images.githubusercontent.com/99194827/228090227-34a9c702-6468-4979-871d-12bea89a86f8.png)
- Open new terminal and access vm in the new terminal using ssh (same as before). Access same container by checking its id and run with exec command.
  ```bash
  docker ps -a
  ```
  Remember CONTAINER ID of the container. This id will be used to access its bash terminal.
  ```bash
  docker exec -it <container-id> bash
  ```
  Replace `<container-id>` with CONTAINER ID above.
  ![image](https://user-images.githubusercontent.com/99194827/229264890-4972df8c-5e71-466d-91ba-0caa46acae3d.png)

## Create, Apply, and Run Prefect Deployment
- To create and apply Prefect Deployment and set the cron to run monthly, execute this command.
  ```bash
  prefect deployment build /app/src/data_pipeline.py:etl_main_function -n "ETL_GCS_to_BGQ_Monthly" --cron "0 0 1 * *" -a
  ```
  A Deployment (as same as job being scheduled) has been built and will be run monthly at 1st day of the month.
  ![image](https://user-images.githubusercontent.com/99194827/228199147-79b85c4e-5b77-4b7e-89fe-0a1e0889d3e0.png) <br>
  
  _LOGICAL FRAMEWORK_ <br>
  _I've created [data_pipeline.py](https://github.com/ahmdxrzky/de-zoomcamp-2023/blob/main/final_project/src/data_pipeline.py) that contains data pipeline consists of: A flow, a subflow, two subsubflows with 3 tasks in each subsubflow._
  1. _A flow called **etl_main_function** that accepts 3 params, which means this flow is parameterized. It will ingest initial dataset or ingest previous month data depends on value of **initial** param._
  2. _A sub flow called **etl_for_a_month** that accepts 2 param (year and month) and handles ingest process of a file of data per month._
  3. _Two subsubflows called **etl_ingest_to_data_lake** and **etl_ingest_to_data_warehouse**. **etl_ingest_to_data_lake** subsubflow consists of 3 tasks, which are **extract_from_source** (Read csv file as dataframe), **write_parquet_to_local** (Transform dataframe to parquet file), and **write_parquet_to_gcs** (Upload parquet file to Data Lake). **etl_ingest_to_data_warehouse** subsubflow consists of 3 tasks too, which are **extract_from_gcs** (Download parquet files from Data Lake), **read_parquet_as_dataframe** (Read parquet file as dataframe), and **write_dataframe_to_gbq** (Ingest dataframe to Data Warehouse)._
  
- Do quick run to ingest initial dataset (Jan 2015 to Feb 2023), since March 1st, 2023 has already passed.
  ```bash
  prefect deployment run etl-main-function/ETL_GCS_to_BGQ_Monthly --param initial=True
  ```
- Don't forget to start a Prefect Agent for the deployment by executing command below:
  ```bash
  prefect agent start -q 'default'
  ```
  By executing command above, quick run to ingest initial dataset will run. BigQuery will start to store dataset from Jan 2015 to Feb 2023.
  ![image](https://user-images.githubusercontent.com/99194827/228421509-62e3fe15-5181-46a9-8b39-e18d3a25455b.png) <br>
  It is also schedule batch processing data of Mar 2023 at Apr 1st, Apr 2023 at May 1st, May 2023 at June 1st, etc <br>
  ![image](https://user-images.githubusercontent.com/99194827/228478394-b8cc0348-d252-4e1f-b9ed-e407c40532f9.png)

### Data Transformation on Data Warehouse with dbt Cloud
- Access dbt cloud [here](https://cloud.getdbt.com/login). Register as usual if you have never create one. Click gear icon on top right side. Then, click **Account Settings**.
  ![image](https://user-images.githubusercontent.com/99194827/228206587-74e90eb9-ea0a-437b-bc2a-eb629d9dbdef.png)
- Click **+ New Project**. Fill name for this project. Then, click **Continue**.
  ![image](https://user-images.githubusercontent.com/99194827/228201875-81b7d241-3e6f-486b-8293-1e11f7a0c11f.png)
- Choose a connection. For this project, choose **BigQuery**. Upload service account keyfile that has been downloaded before.
  ![image](https://user-images.githubusercontent.com/99194827/228202847-e169514d-22bc-4367-842c-cebf5434b988.png)
- In **Development Credentials** part, fill "final_project" in Dataset as we define this dataset with Terraform before. Then, click **Test Connection**. This final_project dataset used as Data Source and Testing Environment before applying Data Modelling schema, since we ingest data from GCS to this GBQ dataset.
  ![image](https://user-images.githubusercontent.com/99194827/228203128-88b8de68-83e9-4489-93f6-93783ea225b9.png)
- In **Setup a Repository** part, click **Github** to choose a repository for dbt versioning.
  You can fork this repository, since dbt configuration folder are on [this folder](https://github.com/ahmdxrzky/de-zoomcamp-2023/tree/main/final_project/dbt) and choose this repository in **Setup a Repository** part. <br>
- Go to **Develop** tab. Execute this command on dbt terminal.
  ```bash
  dbt seed
  dbt run
  ```
  ![image](https://user-images.githubusercontent.com/99194827/228480443-2c7144ca-ea66-4019-9c5f-69b07fd22ce9.png)
  If it run well, then we can proceed to Deployment.
- Drop down **Deploy** and click **Environments**.
  ![image](https://user-images.githubusercontent.com/99194827/228686465-38acffd4-5d10-488b-8fa0-54548dbdd1b8.png)
- Click **Create Environment**. Because development environment has been already built, we can only create deployment environment. Fill in **Name** as name for this deployment environment and **Dataset** as name of dataset that will be used as final data warehouse after data transformation and used for visualization.
  ![image](https://user-images.githubusercontent.com/99194827/228686925-c3a376cd-15f1-4835-b667-6161a6631c80.png)
- It is automatically redirecting us to the environment dashboard menu. Click **+ Create One**. Fill in **Job Name** and **Target Name**. Don't forget to make this target name here differs with target name on Dev Environment.
  ![image](https://user-images.githubusercontent.com/99194827/228687956-b1f7f706-2a47-428b-ab64-bae4313d215e.png)
- Add commands that want to be run within the model. Since we only need two chunks of code in development to create everything, then we only need to write down these two commands.
  ![image](https://user-images.githubusercontent.com/99194827/228688156-7631c9de-1007-4ae0-8a26-1d2e5a436a77.png)
- Click the job that has been built just now and click **Run Now** to see if deployment process can be run or not.
  ![image](https://user-images.githubusercontent.com/99194827/228703172-ebd7c212-9868-449d-9497-11b0a73dc194.png)
- As a result, source and staging table are in different datasets.
  ![image](https://user-images.githubusercontent.com/99194827/228703208-3c63d718-8570-4e0a-b1d6-b7cffe8de5db.png)
  
  _LOGICAL FRAMEWORK_ <br>
  1. _**dbt** initiates a folder as data modelling schema by creating folders. It uses external file as data source for table if the file is being put in **seeds** folder. It also creates models if the models' schema are defined in **models** folder._
  2. _I use [weather_lookup.csv](https://github.com/ahmdxrzky/dbt-cloud-data-transformation/blob/main/seeds/weather_lookup.csv) as seed file. It contains weather id used in weather data that corresponds with its weather name and description._
  3. _I define two kinds of model schema, which are **staging** and **facts**._
  4. _I define a [staging model](https://github.com/ahmdxrzky/dbt-cloud-data-transformation/blob/main/models/staging/stg_weather_data.sql) as **view** in GBQ. It takes several columns from partitioned **all_weather_data** table and converts their data types._
  5. _I define a [**dimensional table**](https://github.com/ahmdxrzky/dbt-cloud-data-transformation/blob/main/models/facts/dim_weather.sql) from seed file._
  6. _I define a [**fact table**](https://github.com/ahmdxrzky/dbt-cloud-data-transformation/blob/main/models/facts/fact_weather.sql) which join weather data with dimensional table based on weather_id._

### Data Visualization with Looker Data Studio
- Access Looker Data Studio [here](https://lookerstudio.google.com) and login with google account. Then, click **Create** then **Data source**.
  ![image](https://user-images.githubusercontent.com/99194827/228208676-08ab15b4-294c-4ff1-b3f2-7884c1ed25ff.png)
- Choose **BigQuery**.
  ![image](https://user-images.githubusercontent.com/99194827/228208786-4607c008-5772-420e-bee4-baccffe30b0b.png)
- Choose project, dataset, and table on BigQuery that will be used as data source. Then, click **Connect**. For this project, I used fact table defined from Data Transformation with dbt.
  ![image](https://user-images.githubusercontent.com/99194827/229086381-9b4d8875-bd36-419d-920f-4f90bf6f78c1.png)
- Click **Create** then **Report**.
  ![image](https://user-images.githubusercontent.com/99194827/228209589-574d4bad-15ab-48c5-b969-5697bed9ab46.png)
- Define dashboard as your wish. My dashboard project can be accessed [here](https://lookerstudio.google.com/reporting/ece80e5f-5838-47eb-ba58-b64ff5576b1c)
  ![Screenshot 2023-04-01 112809](https://user-images.githubusercontent.com/99194827/229265595-575a93d4-6895-43d5-bb04-170960a4ee34.png)
  
  _LOGICAL FRAMEWORK_ <br>
  1. _The first visualization is created using three columns. I use **record_datetime** as filter, **record_month** as x-axis, and count of **weather_category** per month as y-axis. I also use **weather_category** itself as detail dimension._
  2. _The second visualization is created using two columns. I use **record_datetime** as filter and x-axis also average of **temperature** on a day as y-axis._

# Insights and Goals Fulfilling
A data pipeline of Denpasar Weather Data from data source to dashboard has been **created**. From visualization of data, it can be clearly seen that month with highest total of rainy day is **January** and the lowest is **October**, where October is assumed as **rainy** season. Therefore, I strongly believe that there is a **shift** in weather patternal in Denpasar.

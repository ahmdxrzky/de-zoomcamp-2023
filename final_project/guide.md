# Problem Statement
Pattern of weather is getting more difficult to be identified year by year. There are many factors led to this phenomenon, especially global warming. Usually, Indonesian people could be certain that the dry season would occur from March to September and the rainy season on the other hand. Now, we can no longer use this knowledge as reference. Therefore, I am interested to build this project in order to answer the question of _whether there have been changes in weather patterns in Indonesia or not_.

# Data Source
#### [_Denpasar Weather Data on Kaggle_](https://www.kaggle.com/datasets/cornflake15/denpasarbalihistoricalweatherdata?resource=download) ####
Disclaimer: Actually, dataset above only provides weather data of Denpasar City from 1990 to 2020 (even the data for 2020 is not complete to December). In order to make this data engineering project (which batch processes the data) look real and simulate the actual workflow of data engineering, I _manipulate_ the dataset by _adding_ 4 years to the actual date data and _dividing_ it per year and month, so the data for 2023 are available and can be used to simulate batch processing per month.

# Project Framework
![assets](https://user-images.githubusercontent.com/99194827/227752387-4736cd2d-ecf3-4579-a40e-1558f48d6413.png)
1. Pipeline for processing dataset and extracting it from source to a data lake.
2. Pipeline for batch moving the data from the data lake to a data warehouse.
3. Transform the data in the data warehouse.
4. Create a dashboard to see pattern of weather by year.

# Tools
### Cloud
- **Google Compute Engine (GCE)**. A GCE virtual machine used to develop and run this project along with Google Cloud Storage (GCS) and Google BigQuery (GBQ).
- **Terraform**. Infrastructure as Code (IaC) tool to create a GCS Bucket and GBQ Dataset in a code execution only.
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
- Grant all access needed by this service account to the project. Since this project will work around Cloud Storage and BigQuery, so I grant these roles for this service account. Then, click **Continue**. Then, click **Done** on bottom of the page.
  ![Screenshot 2023-03-28 051754](https://user-images.githubusercontent.com/99194827/228079475-2a304a14-01ae-4646-ab5f-b710d20203a9.png)
- Click three dots on row of the newly built Service Account and click **Manage keys**.
  ![Screenshot 2023-03-28 052039](https://user-images.githubusercontent.com/99194827/228079986-950b8695-1e61-4fd0-8d1e-20476df5b441.png)
- Drop **Add key** down, then click **Create new key**.
  ![Screenshot 2023-03-28 052151](https://user-images.githubusercontent.com/99194827/228080151-dd07124c-5182-46d1-9d7e-2d4ddc656426.png)
- Choose **JSON** option, then click **Create**. A keyfile in json format will be downloaded automatically.
  ![Screenshot 2023-03-28 052232](https://user-images.githubusercontent.com/99194827/228080289-f73e2675-3bf9-44f3-b6a1-dd6a812852cf.png)

### Create a Virtual Machine Instance on Google Compute Engine
- Still in Google Cloud Console, move to **VM Instances** tab.
  ![Screenshot 2023-03-28 052449](https://user-images.githubusercontent.com/99194827/228080597-900e3bb8-96b9-4e12-b1b4-f81a03683aa3.png)
- Click **Create Instance**.
  ![Screenshot 2023-03-28 052531](https://user-images.githubusercontent.com/99194827/228080697-2cf00073-8e38-48c3-a1ff-012784f3a330.png)
- Fill in name, region, and zone.
  ![Screenshot 2023-03-28 052637](https://user-images.githubusercontent.com/99194827/228080851-981302b9-4a28-49fe-8839-6d1463c60b37.png)
- Scroll down. In Firewall part, allow **HTTP** and **HTTPS** traffic.
  ![Screenshot 2023-03-28 052723](https://user-images.githubusercontent.com/99194827/228081008-64cd7a46-d291-4eb5-839e-11c373d19493.png)
- Scroll down again and drop **Advanced options** down. Drop **Networking** down, fill in network tags and enable **IP forwarding**. Then, click **Create** on bottom of the page.
  ![Screenshot 2023-03-28 052913](https://user-images.githubusercontent.com/99194827/228081268-5154c229-14d0-47e1-bf8c-826f2aaba207.png)
- Remember value from **External IP** column. It will be used for accessing this VM from local machine.
  ![Screenshot 2023-03-28 053032](https://user-images.githubusercontent.com/99194827/228081528-30053ed9-8a82-48d6-b9e1-ec2cf55b1f86.png)
- Move to **Firewall** tab. Then, click **Create Firewall Rule**.
  ![Screenshot 2023-03-28 053143](https://user-images.githubusercontent.com/99194827/228081668-97d46b2e-6e3c-43a7-8aa3-ff07643cf54a.png)
  ![Screenshot 2023-03-28 053232](https://user-images.githubusercontent.com/99194827/228085307-0d8c1bac-d9fa-4545-8509-824f9957472e.png)
- Fill in name and description of firewall rule.
  ![Screenshot 2023-03-28 053336](https://user-images.githubusercontent.com/99194827/228081917-55e32bf8-7662-4a80-9360-236cf464dcb9.png)
- Fill in **target tags** with **network tags** defined previously ("project" for my case), "0.0.0.0/0" on **Source IPv4 ranges** (so all external machine can access this VM), and 4200 on TCP **ports** (port for Prefect UI). Then, click **Create** on bottom of the page.
  ![Screenshot 2023-03-28 053556](https://user-images.githubusercontent.com/99194827/228082396-ce6819db-415a-42bb-bc11-6997f2ca55e8.png)
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
- Back to **Google Cloud Console**. Go to **VM Instances** tab and click previously built VM instance.
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
  ![Screenshot 2023-03-28 054703](https://user-images.githubusercontent.com/99194827/228083970-62a10890-d508-4384-91d5-9756529ae59f.png)

### Clone Github Repository to Virtual Machine
- Install git on virtual machine.
  ```bash
  sudo apt-get install git -y
  ```
- In virtual machine terminal, clone this [github repository](https://github.com/ahmdxrzky/de-zoomcamp-2023). Then, change working directory to final_project folder.
  ```bash
  git clone https://github.com/ahmdxrzky/de-zoomcamp-2023.git && cd de-zoomcamp-2023/final_project
  ```
- Copy contents of keyfile previously downloaded to replace content in the config/keyfile.json file. <br>
  Before: <br>
  ![Screenshot 2023-03-28 060505](https://user-images.githubusercontent.com/99194827/228086611-ea35c539-5b90-4566-9807-29799240608c.png) <br>
  After: <br>
  ![Screenshot 2023-03-28 060521](https://user-images.githubusercontent.com/99194827/228086639-eb88867c-22cb-4afa-8cd2-336c0d6ec04d.png)
- Check project id. <br>
  Personal project id can be seen in google cloud console.
  ![Screenshot 2023-03-29 093459](https://user-images.githubusercontent.com/99194827/228412084-a15023e3-2fe5-4823-ab0a-614b3a7caf3d.png)
- Change `<gcp-project-id>` string on Dockerfile and variables.tf file on terraform folder with your personal project id. This process can be done in a single execution like this.
  ```bash
  python3 src/manipulation_project_id.py <project-id>
  ```
  Replace `<project-id>` with personal project id seen from cloud console in previous step.
  
### Build Docker Image and Run Docker Container
- Install docker on virtual machine.
  ```bash
  sudo apt-get install docker.io -y
  sudo chmod 666 /var/run/docker.sock
  ```
- Still in final_project working directory, build docker image based on Dockerfile
  ```bash
  docker build -t rizky_dezoomcamp_final_project ./
  ```
- Run docker container based on previously built docker image also exposing port 4200 for Prefect UI.
  ```bash
  docker run -p 4200:4200 -it rizky_dezoomcamp_final_project
  ```

### Activate and Configurate Prefect
- Activate and Access Prefect UI.
  ```bash
  prefect config set PREFECT_API_URL=http://<external-ip>:4200/api
  prefect server start --host 0.0.0.0
  ```
  Now, Prefect UI can be accessed from web browser with URL `<external-ip>:4200`. Replace `<external-ip>` with external IP address of the VM.
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
  Fill `gcs-bucket-final-project` for the block on **Block Name**, `dezoomcamp_final_project` on **Bucket**, and choose which GCP Credentials embedded with the bucket on **Gcp Credentials**. Then, click **Create**. <br>
  ![image](https://user-images.githubusercontent.com/99194827/228090227-34a9c702-6468-4979-871d-12bea89a86f8.png)
- Open new terminal and access vm in the new terminal using ssh (same as before). Access same container by checking its id and run with exec command.
  ```bash
  docker ps -a
  docker exec -it <container-id> bash
  ```
  Replace `<container-id>` with container id shown in output of command `docker ps -a`. <br>
  ![Screenshot 2023-03-28 062241](https://user-images.githubusercontent.com/99194827/228088746-9e988e0a-998a-484a-a7ee-d6558460ce58.png)

## Create, Apply, and Run Prefect Deployment
- To create and apply Prefect Deployment and set the cron to run monthly, execute this command.
  ```bash
  prefect deployment build /app/src/data_pipeline.py:etl_main_function -n "ETL_GCS_to_BGQ_Monthly" --cron "0 0 1 * *" -a
  ```
  ![image](https://user-images.githubusercontent.com/99194827/228199147-79b85c4e-5b77-4b7e-89fe-0a1e0889d3e0.png) <br>
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
- In **Development Credentials** part, fill "final_project" in Dataset as we define this dataset with Terraform before. Then, click **Test Connection**.
  ![image](https://user-images.githubusercontent.com/99194827/228203128-88b8de68-83e9-4489-93f6-93783ea225b9.png)
  Until here, we have created a development environment for testing our query and request of data modelling.
- In **Setup a Repository** part, click **Github** to choose a repository for dbt versioning.
  You can fork [this repository](https://github.com/ahmdxrzky/dbt-cloud-data-transformation) and choose this repository in **Setup a Repository** part. <br>
- Click gear icon on top right side. Then, click **Profile Settings**.
  ![Screenshot 2023-03-30 055101](https://user-images.githubusercontent.com/99194827/228685354-43563bf4-ac51-4e22-8b52-e16a00062b69.png)
- Scroll down and copy value from **API Key**.
  ![image](https://user-images.githubusercontent.com/99194827/228685462-ba8b0462-035b-443a-9d0b-aeb393c95d65.png)
- Go to Github repository that has been focked just before. Go to **Settings** and click **Deploy Keys**. Then, click **Add deploy key**.
  ![Screenshot 2023-03-30 055403](https://user-images.githubusercontent.com/99194827/228695052-67e5b4d4-7ad3-45cd-9ccf-0360fae20d6a.png)
- Fill in **Title** and copy copied key to **Key**. Don't forget to checklist **Allow write access** part.
  ![image](https://user-images.githubusercontent.com/99194827/228686230-d6cc02c9-7ed1-44f6-87dc-9c3901f53331.png)
- Go to **Develop** tab. Execute this command on dbt terminal.
  ```bash
  dbt seed
  dbt run
  ```
  ![image](https://user-images.githubusercontent.com/99194827/228480443-2c7144ca-ea66-4019-9c5f-69b07fd22ce9.png)
  If it run well, then we can proceed to Deployment.
- Drop down **Deploy** and click **Environments**.
  ![image](https://user-images.githubusercontent.com/99194827/228686465-38acffd4-5d10-488b-8fa0-54548dbdd1b8.png)
- Click **Create Environment**. Because development environment has been already built, we can only create deployment environment. Fill in **Name** and **Dataset** name for this deployment environment.
  ![image](https://user-images.githubusercontent.com/99194827/228686925-c3a376cd-15f1-4835-b667-6161a6631c80.png)
- It is automatically redirecting us to the environment dashboard menu. Click **+ Create One**. Fill in **Job Name** and **Target Name**.
  ![image](https://user-images.githubusercontent.com/99194827/228687956-b1f7f706-2a47-428b-ab64-bae4313d215e.png)
- Add commands that want to be run within the model. Since we only need two chunks of code in development to create everything, then we only need to write down these two commands.
  ![image](https://user-images.githubusercontent.com/99194827/228688156-7631c9de-1007-4ae0-8a26-1d2e5a436a77.png)
- Click the job that has been built just now and click **Run Now** to see if deployment process can be run or not.
- 

### Data Visualization with Looker Data Studio
- Access Looker Data Studio [here](https://lookerstudio.google.com) and login with google account. Then, click **Create** then **Data source**.
  ![image](https://user-images.githubusercontent.com/99194827/228208676-08ab15b4-294c-4ff1-b3f2-7884c1ed25ff.png)
- Choose **BigQuery**.
  ![image](https://user-images.githubusercontent.com/99194827/228208786-4607c008-5772-420e-bee4-baccffe30b0b.png)
- Choose project, dataset, and table on BigQuery that will be used as data source. Then, click **Connect**.
  ![image](https://user-images.githubusercontent.com/99194827/228209201-f62779bb-f196-4c44-b047-c9c34b46d982.png)
- Click **Create** then **Report**.
  ![image](https://user-images.githubusercontent.com/99194827/228209589-574d4bad-15ab-48c5-b969-5697bed9ab46.png)
- Define dashboard as your wish. My dashboard project can be accessed [here](https://lookerstudio.google.com/reporting/ece80e5f-5838-47eb-ba58-b64ff5576b1c)
  ![image](https://user-images.githubusercontent.com/99194827/228429331-03a18479-7eb2-40fe-94c1-b32bea70221f.png)
  
# Insights and Goals Fulfilling
From visualization of data, it can be clearly seen that month with highest total of rainy day is January and the lowest is October, where October is assumed as rainy season. Therefore, we strongly believe that there is a shift in weather patternal in Denpasar.

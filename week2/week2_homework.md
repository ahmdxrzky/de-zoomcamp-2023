# Answer for Homework Week 2

## Question 1
Execute [this python file](https://github.com/ahmdxrzky/de-zoomcamp-2023/blob/main/week2/etl_web_to_gcs.py) with command below to loads _Green Taxi Trip on Jan 2020_ data to GCS:
```bash
python3 etl_web_to_gcs.py
```
There are several edits done to the python file:
1. Pass color parameter to _clean_ function and use it for if-elif conditional, because there are differences of column names that needed fixing of dtype between green and yellow taxi dataset.
2. Add total row of dataset as a return value of _clean_ and _etl_web_to_gcs_ functions.
3. Create parent folders based on parquet file path (take the parent directory path from file path with pathlib) on _write_local_ function, if there is no such directory.
4. Set color, year, and month as parameters of _etl_web_to_gcs_ function.

To see logs from the flow above, execute command below to activate the Prefect UI:
```bash
prefect orion start
```
Click the latest flow run on Flow Runs menu. Then, click Logs tab to see recorded logs from that flow run.<br>
Result:
![image](https://user-images.githubusercontent.com/99194827/216642020-bb3901f8-88cd-478d-bfa5-f35fa2425867.png)
From image above, it can be clearly seen that there are _447770_ rows on data of Green Taxi Trip on Jan 2020.

## Question 2
### First Way (through Prefect UI)
Execute command below to build a prefect deployment named as _ETL-to-GCS_ based on _etl_web_to_gcs_ flow from [this python file](https://github.com/ahmdxrzky/de-zoomcamp-2023/blob/main/week2/etl_web_to_gcs.py):
```bash
prefect deployment build ./etl_web_to_gcs.py:etl_web_to_gcs -n "ETL-to-GCS"
```
Command above will generate a YAML file contains configurations for the deployment. Next, execute command below to apply that deployment to prefect:
```bash
prefect deployment apply etl_web_to_gcs-deployment.yaml
```
Edit the deployment configuration on Prefect UI. Move to "Scheduling" part and "Add schedule". Choose "Cron" on "Schedule type" and type in ```0 5 1 * *``` on "Value", then click Save.
![image](https://user-images.githubusercontent.com/99194827/216657927-97a8eb6b-8188-4167-b2bf-8d7ec39de41e.png)
From image above, it can be clearly seen that ```0 5 1 * *``` on cron part simply means _At 05:00 AM (UTC on default) on day 1 of the month_

### Second Way (through terminal)
Execute command below to build and apply a prefect deployment named _ETL-to-GCS_ based on _etl_web_to_gcs_ flow from [this python file](https://github.com/ahmdxrzky/de-zoomcamp-2023/blob/main/week2/etl_web_to_gcs.py) with cron schedule set to "0 5 1 * *":
```bash
prefect deployment build ./etl_web_to_gcs.py:etl_web_to_gcs -n "ETL-to-GCS" --cron "0 5 1 * *" -a
```
```cron "0 5 1 * *"``` means that "0 5 1 \* \*" is passed as cron parameter to set the deployment scheduled run _At 05:00 AM (UTC on default) on day 1 of the month_.
![image](https://user-images.githubusercontent.com/99194827/216754210-d3b7e9ff-6d89-4a32-9734-772ef12218b3.png)
A deployment are enabled on the Prefect UI with no need to edit the configuration anymore, since it's already defined when build the deployment. <br>
Result: <br>
_"0 5 1 \* \*_ in cron syntax means _At 05:00 AM UTC on day 1 of the month_. <br>

### Additional things:
After sure that the deployment is already deployed on prefect, don't forget to execute command below to activate an agent to run flow of that deployment (in this case, an agent named _default_):
```bash
prefect agent start -q default
```

## Question 3
Before focus on the ETL from GCS to GBQ, make sure that _Yellow Taxi Trip on February and March 2019_ data have already on the GCS. It can be easily done by running the deployment used in Q2 above two times (after activate a prefect agent) with these commands below:
```bash
prefect deployment run etl-web-to-gcs/ETL-to-GCS -p "color=yellow" -p "year=2019" -p "month=2"
prefect deployment run etl-web-to-gcs/ETL-to-GCS -p "color=yellow" -p "year=2019" -p "month=3"
```
After all data that want to be migrated have already on GCS, execute command below to build and apply a prefect deployment named _ETL-to-GBQ_ based on _etl_gcs_to_bq_ flow from [this python file](https://github.com/ahmdxrzky/de-zoomcamp-2023/blob/main/week2/etl_gcs_to_bq.py):
```bash
prefect deployment build ./etl_gcs_to_bq.py:etl_main_flow -n "ETL-to-GBQ" -a
```
There are several edits done to the python file:
1. Adjust local path on and return value from _extract_from_gcs_ also destination table and project_id on _write_bq_ function.
2. Delete _transform_ function and move read from parquet to _etl_gcs_to_bq_ function, since no transformation and cleaning process needed.
3. Use total row from the dataset that being migrated to BigQuery as returned value from _write_bq_ and _etl_gcs_to_bq_ functions.
4. Set log prints parameter as True on _etl_main_flow_ flow declaration and add command print to its body, so logs will record total rows that being migrated.
5. Set "yellow", 2019, and [2, 3] as default value of color, year, and months variables on _etl_main_flow_ function, because we want to migrate _Yellow Taxi Trips on February and March 2019_ data.

Execute command below to activate a prefect agent (in this case, an agent named _default_):
```bash
prefect agent start -q default
```
Last, execute command below on a different terminal to run that deployment:
```bash
prefect deployment run etl-main-flow/ETL-to-GBQ
```
See logs of latest flow run on Prefect UI. <br>
Result:
![image](https://user-images.githubusercontent.com/99194827/216754941-50b916ed-dee7-4741-8ead-eeb6bded2825.png)
From image above, it can be clearly seen that there are _14851920_ data being migrated from GCS to BigQuery.

## Question 4
Create a GitHub storage block on Prefect UI.
![image](https://user-images.githubusercontent.com/99194827/216757198-e69e0546-4de8-432f-8401-91df1db08bc7.png)
Next, upload the flow file to some github repository. In my case, I already upload the file [here](https://github.com/ahmdxrzky/de-zoomcamp-2023/blob/main/week2/etl_web_to_gcs.py). <br>
Then, execute [this python file](https://github.com/ahmdxrzky/de-zoomcamp-2023/blob/main/week2/github_deploy.py) to build and apply a prefect deployment named _store-to-github_ based on _etl_web_to_gcs_ flow from python file that already uploaded on github before:
```bash
python3 github_deploy.py
```
Next, execute command below to activate a prefect agent (in this case, an agent named _default_):
```bash
prefect agent start -q default
```
Last, execute command below on a different terminal to run that deployment:
```bash
prefect deployment run etl-web-to-gcs/store-to-github -p "month=11"
```
See logs of latest flow run on Prefect UI. <br>
Result:
![image](https://user-images.githubusercontent.com/99194827/216811597-62a624ae-31f7-4e3f-8ab7-ef4b9af0e56b.png)
From image above, it can be clearly seen that there are _88605_ rows on data of Green Taxi Trip on Nov 2020.

## Question 5
First, create a Prefect Cloud account [here](https://app.prefect.cloud).<br>
Next, create a workspace to be connected with local machine.<br>
Then, login to Prefect Cloud in the terminal by executing command below:
```bash
prefect cloud login
```
Authorize login in browser.<br>
In terms to create notification of flow from this [script](https://github.com/ahmdxrzky/de-zoomcamp-2023/blob/main/week2/etl_web_to_gcs.py), email and gcs blocks have to be created on Prefect Cloud. By default, those two blocks are not available on Prefect Cloud, so those two blocks have to be registered first by executing these command below:
```bash
prefect block register -m prefect_gcp.cloud_store
prefect block register -m prefect_email
```
After that, create _Email Server Credentials_ block and fill in email and password used to username and password, respectively. Create _GCP Credentials_ and _GCS Bucket_ exactly same with same blocks on local machine that being used before.<br>
Last, run [this python file](https://github.com/ahmdxrzky/de-zoomcamp-2023/blob/main/week2/gmail_send.py) by executing command below:
```bash
python3 gmail_send.py
```
See inbox in email that being used as username on _Email Server Credentials_ block. <br>
Result:
![Screenshot 2023-02-05 200906](https://user-images.githubusercontent.com/99194827/216820762-f2d7c248-6413-4671-a61b-269c869b6871.png)
![Screenshot 2023-02-05 201126](https://user-images.githubusercontent.com/99194827/216820934-b948e015-9286-4332-9d81-7d5eea17a6c8.png)
From image above, it can be clearly seen that there are _514392_ rows on data of Green Taxi Trip on April 2019.

## Question 6
Create a _Secret_ block on Prefect UI. That block is used to hide any string that shouldn't be publicly accessible.<br>
Result: <br>
![image](https://user-images.githubusercontent.com/99194827/216824310-95b8ed0a-0d3b-4b7d-9fe2-a808ca88f51f.png)
From image above, it can be clearly seen that the encrypted value shown as _8 asterisks_.

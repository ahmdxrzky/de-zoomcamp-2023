# Answer for Homework Week 2

## Question 1
Executing [this python file](https://github.com/ahmdxrzky/de-zoomcamp-2023/blob/main/week2/etl_web_to_gcs.py) with command below to loads _Green Taxi Trip on Jan 2020_ data to GCS:
```
python3 etl_web_to_gcs.py
```
To see logs from the prefect flow above, execute command below to activate the GUI of prefect and click the link given on the output:
```
prefect orion start
```
Result:
![image](https://user-images.githubusercontent.com/99194827/216642020-bb3901f8-88cd-478d-bfa5-f35fa2425867.png)
From image above, it can be clearly seen that there are _447770_ rows on data of Green Taxi Trip on Jan 2020.

## Question 2
### First Way
Execute command below to build a prefect deployment named as _ETL-to-GCS_ based on _etl_web_to_gcs_ flow from _./etl_web_to_gcs.py_ file:
```
prefect deployment build ./etl_web_to_gcs.py:etl_web_to_gcs -n "ETL-to-GCS"
```
Command above will generate a YAML file contains configurations for the deployment. Next, execute command below to apply that deployment to prefect:
```
prefect deployment apply etl_web_to_gcs-deployment.yaml
```
Everytime a deployment want to be run, execute command below to activate a prefect agent named _default_:
```
prefect agent start -q default
```
Edit the deployment configuration on prefect GUI. Move to Scheduling part and add schedule. Choose "cron" on "Schedule type" and type in ```0 5 1 \* \*``` on "Value", then click Save.
![image](https://user-images.githubusercontent.com/99194827/216657927-97a8eb6b-8188-4167-b2bf-8d7ec39de41e.png)
From image above, it can be clearly seen that ```0 5 1 \* \*``` on cron part simply means _At 05:00 AM (UTC on default) on day 1 of the month_
Last, execute command below on a different terminal to run that deployment:
```
prefect deployment run etl-web-to-gcs/ETL-to-GCS
```

### Second Way (the shorter one, perhaps)
Execute command below to build and apply a prefect deployment named _ETL-to-GCS_ based on _etl_web_to_gcs_ flow from _./etl_web_to_gcs.py_ file with cron schedule set to "0 5 1 * *":
```
prefect deployment build ./etl_web_to_gcs.py:etl_web_to_gcs -n "ETL-to-GCS" --cron "0 5 1 * *" -a
```
```cron "0 5 1 * *"``` means that "0 5 1 \* \*" is passed as cron parameter to set the deployment scheduled run _At 05:00 AM (UTC on default) on day 1 of the month_.<br>
Execute command below to activate a prefect agent named default:
```
prefect agent start -q default
```
Last, execute command below on a different terminal to run that deployment:
```
prefect deployment run etl-web-to-gcs/ETL-to-GCS
```

## Question 3

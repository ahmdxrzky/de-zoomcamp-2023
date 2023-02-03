# Answer for Homework Week 2

## Question 1
Executing [this python file](https://github.com/ahmdxrzky/de-zoomcamp-2023/blob/main/week2/etl_web_to_gcs.py) with command below to loads Green Taxi Trip on Jan 2020 data to GCS:
```
python3 etl_web_to_gcs.py
```
To see logs from the prefect flow above, execute command below on a different terminal to activate the GUI of prefect and click the link given on the output:
```
prefect orion start
```
Result:
![image](https://user-images.githubusercontent.com/99194827/216642020-bb3901f8-88cd-478d-bfa5-f35fa2425867.png)
From image above, it can be clearly seen that there are _447770_ rows on data of Green Taxi Trip on Jan 2020.

## Question 2
### First Way
Execute command below to build a prefect deployment based on etl_web_to_gcs flow from ./etl_web_to_gcs.py file:
```
prefect deployment build ./etl_web_to_gcs.py:etl_web_to_gcs -n "ETL-to-GCS"
```
Command above will generate a YAML file contains configurations for the deployment.<br>
Next, execute command below to apply that deployment to prefect:
```
prefect deployment apply etl_web_to_gcs-deployment.yaml
```
Everytime a deployment want to be run, execute command below to activate a prefect agent (in this case, agent's name being used is default):
```
prefect agent start -q default
```
Edit the deployment configuration on prefect GUI. Move to Scheduling part and add schedule.<br>
Choose "cron" on "Schedule type" and type ```0 5 1 \* \*``` on "Value", so the flow from the deployment will be run _At 05:00 AM (UTC on default) on day 1 of the month_, then click Save.
![image](https://user-images.githubusercontent.com/99194827/216657927-97a8eb6b-8188-4167-b2bf-8d7ec39de41e.png)
Last, execute command below on a different terminal to run that deployment:
```
prefect deployment run etl-web-to-gcs/ETL-to-GCS
```

### Second Way (on the shorter one, perhaps)
Execute command below to build and apply a prefect deployment (and all of its configuration, including the cron schedule) based on etl_web_to_gcs flow:
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

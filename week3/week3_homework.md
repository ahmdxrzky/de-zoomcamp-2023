# Answer for Homework Week 3

## Setup
Before answer the question, there are some important steps that should be done:
#### Load data in .gz format to Google Cloud Storage


## Question 1
Execute [this python file](https://github.com/ahmdxrzky/de-zoomcamp-2023/blob/main/week2/etl_web_to_gcs.py) with command below to loads _Green Taxi Trip on Jan 2020_ data to GCS:
```
python3 etl_web_to_gcs.py
```
There are several edits done to the python file:
1. Pass color parameter to _clean_ function and use it for if-elif conditional, because there are differences of column names that needed fixing of dtype between green and yellow taxi dataset.
2. Add total row of dataset as a return value of _clean_ and _etl_web_to_gcs_ functions.
3. Create parent folders based on parquet file path (take the parent directory path from file path with pathlib) on _write_local_ function, if there is no such directory.
4. Set color, year, and month as parameters of _etl_web_to_gcs_ function.

To see logs from the flow above, execute command below to activate the Prefect UI:
```
prefect orion start
```
Click the latest flow run on Flow Runs menu. Then, click Logs tab to see recorded logs from that flow run.<br>
Result:
![image](https://user-images.githubusercontent.com/99194827/216642020-bb3901f8-88cd-478d-bfa5-f35fa2425867.png)
From image above, it can be clearly seen that there are _447770_ rows on data of Green Taxi Trip on Jan 2020.

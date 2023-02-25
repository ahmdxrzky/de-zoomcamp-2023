# Answer for Homework Week 4

## Setup
(Disclaimer: all queries used as answer are already in [this file](https://github.com/ahmdxrzky/de-zoomcamp-2023/blob/main/week4/big_query.sql).<br>
Before answer the questions, there are some important steps that should be done:

#### Load all data in .gz format to Google Cloud Storage
Execute command below to install library needed:
```
pip install pyarrow google-cloud-storage
```
Setup these environment variables by executing command below:
```
export GOOGLE_APPLICATION_CREDENTIALS='path_to_json_file_contains_your_service_account_configuration
export GCP_GCS_BUCKET='name_of_your_GCS_bucket'
```
Execute [this python file](https://github.com/ahmdxrzky/de-zoomcamp-2023/blob/main/week4/web_to_gcs.py) with command below to load _Green and Yellow Trip data along 2019 and 2020 also FHV Trip data along 2019_ in .gz format to GCS:
```
python3 etl_web_to_gcs.py
```
Important notes about the file above:
1. Link for downloading data changed, since the old one is broken.
2. File downloaded to local and uploaded to GCS as gz file. When file uploaded as parquet, errors about different data type between parquet column and bigquery field raised. When file uploaded as CSV, it took so long since size of files are so big.
3. Timeout parameter set to 50000, so timeout error won't be raised when upload process took pretty long time.

#### Create external and local table in BiqQuery with Trip data in GCS
Execute query below on BigQuery to create an external table based on FHV Trips data along 2019 that have been stored on GCS and also its natural table that will be used as source data for data modelling with dbt:
```
CREATE EXTERNAL TABLE IF NOT EXISTS `de-zoomcamp-375916.dezoomcamp.green_tripdata`
OPTIONS (
  format = "CSV",
  uris = ['gs://de-zoomcamp-prefect-2023/data/green/*.csv']
);

CREATE OR REPLACE TABLE `de-zoomcamp-375916.trips_data_all.green_tripdata` AS
SELECT * FROM `de-zoomcamp-375916.dezoomcamp.green_tripdata`;
```
Do the same thing to yellow and FHV data trips by replacing every "green" words with "yellow" and "fhv", respectively.

#### Create source and fact table
Create source table and fact table by running dbt Cloud IDE based on [this repository](https://github.com/ahmdxrzky/dbt-test).<br>
There will be these tables and views structured as below:<br>
![image](https://user-images.githubusercontent.com/99194827/221354453-96924eda-432e-4989-af24-ba0fcdbdbcde.png)

## Question 1
Question: fact_trips records for 2019 and 2020 (test run variable disable) <br>
Logic: Count total record on fact_trips (make sure that the test run variable has been disabled or set to False). <br>
Query:
```
SELECT COUNT(1) AS total_fact_trips
FROM `de-zoomcamp-375916.dbt_test.fact_trips`;
```
Result:
![image](https://user-images.githubusercontent.com/99194827/221353824-5a0156a3-11e9-45de-8a0d-adb74e617138.png)

From images above, it can be clearly seen that there are _61622271_ rows on fact_trips table (when test_run variable disabled). Choose _61648442_ as answer since it's the closest one.

## Question 2
Question: Distribution of service type for data of year 2019 and 2020. <br>
Logic: Visualize data through Google Data Studio. <br>
Result:
![image](https://user-images.githubusercontent.com/99194827/221363053-65b9dee4-3c6b-4974-9670-956ea9bda799.png)

From images above, it can be clearly seen that ratio between Yellow and Green service on 2019 and 2020 is _89.8:10.2_. Choose _89.9/10.1_ as answer since it's the closest one.

## Question 3
Question: stg_fhv_tripdata records for 2019 <br>
Logic:
- Add fhv_tripdata as data source on schema.yml at staging folder.
- Create [stg_fhv_tripdata.sql](https://github.com/ahmdxrzky/dbt-test/blob/main/models/staging/stg_fhv_tripdata.sql) file at staging folder.
- Run that model. <br>
Query:
```
SELECT COUNT(1) AS total_staging_fhv_trips
FROM `de-zoomcamp-375916.dbt_test.stg_fhv_tripdata`;
```
Result:
![image](https://user-images.githubusercontent.com/99194827/221359258-038e0fa9-6cab-40da-939e-f2510f220dc9.png)

From images above, it can be clearly seen that there are _43244696_ rows on stg_fhv_tripdata table.

## Question 4
Question: fact_fhv_trips records for 2019 <br>
Logic:
- Create [fact_fhv_trips.sql](https://github.com/ahmdxrzky/dbt-test/blob/main/models/core/fact_fhv_trips.sql) file at core folder.
- Add fact_fhv_trips on schema.yml at core folder.
- Run that model. <br>
Query:
```
SELECT COUNT(1) AS total_fact_fhv_trips FROM `de-zoomcamp-375916.dbt_test.fact_fhv_trips`;
```
Result:
![image](https://user-images.githubusercontent.com/99194827/221359559-ecb2bea4-867a-426a-b870-fbb72c7686ea.png)

From images above, it can be clearly seen that there are _22998722_ rows on fact_fhv_trips.

## Question 5
Question: Month with highest trip amount. <br>
Logic: Visualize data through Google Data Studio. <br>
Result:
![image](https://user-images.githubusercontent.com/99194827/221365983-491f43ba-61bd-498d-897c-50f7e59681ea.png)

From images above, it can be clearly seen that _January_ has the highest amount of FHV trips.

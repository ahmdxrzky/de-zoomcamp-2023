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

## Question 1
Question: <br>
Logic: <br>
Query:
```
SELECT COUNT(1) AS fhv_vehicle_records_on_2019
FROM `de-zoomcamp-375916.dezoomcamp.fhv_2019_external`;
```
Result:
![image](https://user-images.githubusercontent.com/99194827/217843339-edc11b29-4ad8-4e9d-9d04-91a4250e9978.png)

From images above, it can be clearly seen that there are _43244696_ rows on data of FHV Trip along 2019.

## Question 2
Question: <br>
Logic: <br>
Query:
```
SELECT COUNT(1) AS fhv_vehicle_records_on_2019
FROM `de-zoomcamp-375916.dezoomcamp.fhv_2019_external`;
```
Result:
![image](https://user-images.githubusercontent.com/99194827/217843339-edc11b29-4ad8-4e9d-9d04-91a4250e9978.png)

From images above, it can be clearly seen that there are _43244696_ rows on data of FHV Trip along 2019.

## Question 3
Question: <br>
Logic: <br>
Query:
```
SELECT COUNT(1) AS fhv_vehicle_records_on_2019
FROM `de-zoomcamp-375916.dezoomcamp.fhv_2019_external`;
```
Result:
![image](https://user-images.githubusercontent.com/99194827/217843339-edc11b29-4ad8-4e9d-9d04-91a4250e9978.png)

From images above, it can be clearly seen that there are _43244696_ rows on data of FHV Trip along 2019.

## Question 4
Question: <br>
Logic: <br>
Query:
```
SELECT COUNT(1) AS fhv_vehicle_records_on_2019
FROM `de-zoomcamp-375916.dezoomcamp.fhv_2019_external`;
```
Result:
![image](https://user-images.githubusercontent.com/99194827/217843339-edc11b29-4ad8-4e9d-9d04-91a4250e9978.png)

From images above, it can be clearly seen that there are _43244696_ rows on data of FHV Trip along 2019.

## Question 5
Question: <br>
Logic: <br>
Query:
```
SELECT COUNT(1) AS fhv_vehicle_records_on_2019
FROM `de-zoomcamp-375916.dezoomcamp.fhv_2019_external`;
```
Result:
![image](https://user-images.githubusercontent.com/99194827/217843339-edc11b29-4ad8-4e9d-9d04-91a4250e9978.png)

From images above, it can be clearly seen that there are _43244696_ rows on data of FHV Trip along 2019.

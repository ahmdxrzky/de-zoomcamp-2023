# Answer for Homework Week 3

## Setup
(Disclaimer: all queries used as answer are already in [this file](https://github.com/ahmdxrzky/de-zoomcamp-2023/blob/main/week3/big_query.sql).<br>
Before answer the questions, there are some important steps that should be done:

#### Load data in .gz format to Google Cloud Storage
Execute [this python file](https://github.com/ahmdxrzky/de-zoomcamp-2023/blob/main/week3/etl_gz_to_gcs.py) with command below to load _FHV Trip data along 2019_ in .gz format to GCS:
```
python3 etl_web_to_gcs.py
```
Important notes about the file above:
1. All flows run under supervision of Prefect.
2. It consists of a parent flow and a sub flow with two tasks.
3. All flows defined with _log_prints_ parameter as True and all tasks defined with _retries_ parameter set to 3.
4. Parent flow (_etl_year_):<br>
Dataset splitted per month. To interact with FHV Trip data along 2019, all FHV data per month in 2019 should be retrieved. It done in this parent flow.
5. Sub flow (_etl_month_):<br>
To retrieve data for each month, file need to be downloaded to local with _write_local_ task and uploaded to GCS with _write_gcs_ task.

#### Create external table in BiqQuery with FHV Trip data along 2019 in GCS
Execute query below to create an external table based on FHV Trips data along 2019 that have been stored on GCS:
```
CREATE EXTERNAL TABLE IF NOT EXISTS `de-zoomcamp-375916.dezoomcamp.fhv_2019_external`
  OPTIONS (
    format ="CSV",
    uris = ['gs://de-zoomcamp-prefect-2023/data/fhv/*.gz']
    );
```
Query above indicates that a table named as _fhv_2019_external_ with data sourced from GCS in CSV format.

#### Create table in BigQuery with FHV Trip data along 2019 (no partition and cluster needed == natural table)
Execute query below to create a table from external table created before:
```
CREATE OR REPLACE TABLE `de-zoomcamp-375916.dezoomcamp.fhv_2019_natural` AS
SELECT * FROM `de-zoomcamp-375916.dezoomcamp.fhv_2019_external`
```

## Question 1
Question: FHV vehicle records for year 2019.<br>
Logic: Count total records on the table.<br>
Query:<br>
- on External table
```
SELECT COUNT(1) AS fhv_vehicle_records_on_2019
FROM `de-zoomcamp-375916.dezoomcamp.fhv_2019_external`;
```
- on Natural table
```
SELECT COUNT(1) AS fhv_vehicle_records_on_2019
FROM `de-zoomcamp-375916.dezoomcamp.fhv_2019_natural`;
```
Result:<br>
- on External table
![image](https://user-images.githubusercontent.com/99194827/217843339-edc11b29-4ad8-4e9d-9d04-91a4250e9978.png)
- on Natural table
![image](https://user-images.githubusercontent.com/99194827/217843589-861df26e-7f14-4f9b-8dd4-7c6f5c6107ba.png)

From images above, it can be clearly seen that there are _43244696_ rows on data of FHV Trip along 2019.

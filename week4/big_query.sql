-- SETUP
CREATE EXTERNAL TABLE IF NOT EXISTS `de-zoomcamp-375916.dezoomcamp.green_tripdata`
OPTIONS (
  format = "CSV",
  uris = ['gs://de-zoomcamp-prefect-2023/data/green/*.csv']
);

CREATE OR REPLACE TABLE `de-zoomcamp-375916.trips_data_all.green_tripdata` AS
SELECT * FROM `de-zoomcamp-375916.dezoomcamp.green_tripdata`;

CREATE EXTERNAL TABLE IF NOT EXISTS `de-zoomcamp-375916.dezoomcamp.yellow_tripdata`
OPTIONS (
  format = "CSV",
  uris = ['gs://de-zoomcamp-prefect-2023/data/yellow/*.csv']
);

CREATE OR REPLACE TABLE `de-zoomcamp-375916.trips_data_all.yellow_tripdata` AS
SELECT * FROM `de-zoomcamp-375916.dezoomcamp.yellow_tripdata`;

CREATE EXTERNAL TABLE IF NOT EXISTS `de-zoomcamp-375916.dezoomcamp.fhv_tripdata`
OPTIONS (
  format = "CSV",
  uris = ['gs://de-zoomcamp-prefect-2023/data/fhv/*.csv']
);

CREATE OR REPLACE TABLE `de-zoomcamp-375916.trips_data_all.fhv_tripdata` AS
SELECT * FROM `de-zoomcamp-375916.dezoomcamp.fhv_tripdata`;

-- QUESTION 1
SELECT COUNT(1) AS total_fact_trips FROM `de-zoomcamp-375916.dbt_test.fact_trips`;

-- QUESTION 3
SELECT COUNT(1) AS total_staging_fhv_trips FROM `de-zoomcamp-375916.dbt_test.stg_fhv_tripdata`;

-- QUESTION 4
SELECT COUNT(1) AS total_fact_fhv_trips FROM `de-zoomcamp-375916.dbt_test.fact_fhv_trips`;






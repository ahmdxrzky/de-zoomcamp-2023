-- SETUP
CREATE EXTERNAL TABLE IF NOT EXISTS `de-zoomcamp-375916.dezoomcamp.fhv_2019_external`
OPTIONS (
  format ="CSV",
  uris = ['gs://de-zoomcamp-prefect-2023/data/fhv/*.gz']
);

CREATE OR REPLACE TABLE `de-zoomcamp-375916.dezoomcamp.fhv_2019_natural` AS
SELECT * FROM `de-zoomcamp-375916.dezoomcamp.fhv_2019_external`

-- QUESTION 1
SELECT COUNT(1) AS fhv_vehicle_records_on_2019
FROM `de-zoomcamp-375916.dezoomcamp.fhv_2019_external`;

SELECT COUNT(1) AS fhv_vehicle_records_on_2019
FROM `de-zoomcamp-375916.dezoomcamp.fhv_2019_natural`;

-- QUESTION 2
SELECT COUNT(DISTINCT affiliated_base_number) AS distinct_number_of_affiliated_base_number
FROM `de-zoomcamp-375916.dezoomcamp.fhv_2019_external`;

SELECT COUNT(DISTINCT affiliated_base_number) AS distinct_number_of_affiliated_base_number
FROM `de-zoomcamp-375916.dezoomcamp.fhv_2019_natural`;

-- QUESTION 3
SELECT COUNT(1) AS null_on_PUloc_and_DOloc
FROM `de-zoomcamp-375916.dezoomcamp.fhv_2019_external`
WHERE PUlocationID is null and DOlocationID is null;

SELECT COUNT(1) AS null_on_PUloc_and_DOloc
FROM `de-zoomcamp-375916.dezoomcamp.fhv_2019_natural`
WHERE PUlocationID is null and DOlocationID is null;

-- QUESTION 5
CREATE OR REPLACE TABLE `de-zoomcamp-375916.dezoomcamp.fhv_2019_partitioned_clustered`
PARTITION BY DATE(pickup_datetime)
CLUSTER BY affiliated_base_number AS
SELECT * FROM `de-zoomcamp-375916.dezoomcamp.fhv_2019_natural`;

SELECT COUNT(DISTINCT affiliated_base_number) AS distinct_number_of_affiliated_base_number_along_march_2019
FROM `de-zoomcamp-375916.dezoomcamp.fhv_2019_natural`
WHERE DATE(pickup_datetime) BETWEEN '2019-03-01' AND '2019-03-31';

SELECT COUNT(DISTINCT affiliated_base_number) AS distinct_number_of_affiliated_base_number_along_march_2019
FROM `de-zoomcamp-375916.dezoomcamp.fhv_2019_partitioned_clustered`
WHERE DATE(pickup_datetime) BETWEEN '2019-03-01' AND '2019-03-31';

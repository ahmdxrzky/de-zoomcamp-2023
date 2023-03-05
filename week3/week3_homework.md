# Answer for Homework Week 3
Disclaimer: all queries used as answer are already in [this file](https://github.com/ahmdxrzky/de-zoomcamp-2023/blob/main/week3/big_query.sql).

## Setup
Before answer the questions, there are some important steps that should be done:

#### Load data in .gz format to Google Cloud Storage
Execute [this python file](https://github.com/ahmdxrzky/de-zoomcamp-2023/blob/main/week3/etl_gz_to_gcs.py) with command below to load _FHV Trip data along 2019_ in .gz format to GCS:
```bash
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
```sql
CREATE EXTERNAL TABLE IF NOT EXISTS `de-zoomcamp-375916.dezoomcamp.fhv_2019_external`
  OPTIONS (
    format ="CSV",
    uris = ['gs://de-zoomcamp-prefect-2023/data/fhv/*.gz']
    );
```
Query above indicates that a table named as _fhv_2019_external_ with data sourced from GCS in CSV format.

#### Create table in BigQuery with FHV Trip data along 2019 (no partition and cluster needed == natural table)
Execute query below to create a table from external table created before:
```sql
CREATE OR REPLACE TABLE `de-zoomcamp-375916.dezoomcamp.fhv_2019_natural` AS
SELECT * FROM `de-zoomcamp-375916.dezoomcamp.fhv_2019_external`
```

## Question 1
Question: FHV vehicle records for year 2019.<br>
Logic: Count total records on the table.<br>
Query:<br>
- on External table
  ```sql
  SELECT COUNT(1) AS fhv_vehicle_records_on_2019
  FROM `de-zoomcamp-375916.dezoomcamp.fhv_2019_external`;
  ```
- on Natural table
  ```sql
  SELECT COUNT(1) AS fhv_vehicle_records_on_2019
  FROM `de-zoomcamp-375916.dezoomcamp.fhv_2019_natural`;
  ```
Result:<br>
- on External table
  ![image](https://user-images.githubusercontent.com/99194827/217843339-edc11b29-4ad8-4e9d-9d04-91a4250e9978.png)
- on Natural table
  ![image](https://user-images.githubusercontent.com/99194827/217843589-861df26e-7f14-4f9b-8dd4-7c6f5c6107ba.png)

From images above, it can be clearly seen that there are _43244696_ rows on data of FHV Trip along 2019.

## Question 2
Question: Estimated amount of data for query of counting distinct number of _affiliated_base_number_ on both tables.<br>
Logic:<br>
- Take rows with distinct value of affiliated_base_number.
- Count total rows.

Query:<br>
- on External table
  ```sql
  SELECT COUNT(DISTINCT affiliated_base_number) AS distinct_number_of_affiliated_base_number
  FROM `de-zoomcamp-375916.dezoomcamp.fhv_2019_external`;
  ```
- on Natural table
  ```sql
  SELECT COUNT(DISTINCT affiliated_base_number) AS distinct_number_of_affiliated_base_number
  FROM `de-zoomcamp-375916.dezoomcamp.fhv_2019_natural`;
  ```
Result:<br>
- on External table
  ![image](https://user-images.githubusercontent.com/99194827/217848526-71421b6d-44ae-4a97-b696-d4af428f7948.png)
- on Natural table
  ![image](https://user-images.githubusercontent.com/99194827/217848702-66bee11f-ba9e-43b3-8064-047601a4e825.png)

From images above, it can be clearly seen that there are _0 B_ and _317.94 MB_ data will be processed on external and natural table, respectively.

## Question 3
Question: Records with null _PUlocationID_ and _DOlocationID_.<br>
Logic:<br>
- Take rows that have null value on PUlocationID and DOlocationID.
- Count total rows.

Query:<br>
- on External table
  ```sql
  SELECT COUNT(1) AS null_on_PUloc_and_DOloc
  FROM `de-zoomcamp-375916.dezoomcamp.fhv_2019_external`
  WHERE PUlocationID is null and DOlocationID is null;
  ```
- on Natural table
  ```sql
  SELECT COUNT(1) AS null_on_PUloc_and_DOloc
  FROM `de-zoomcamp-375916.dezoomcamp.fhv_2019_external`
  WHERE PUlocationID is null and DOlocationID is null;
  ```
Result:<br>
- on External table
  ![image](https://user-images.githubusercontent.com/99194827/217850046-36ebb41b-ce11-46b5-8778-63574bc79a84.png)
- on Natural table
  ![image](https://user-images.githubusercontent.com/99194827/217850385-7cf1008c-4594-497f-8ecb-6c9a91007a22.png)

From images above, it can be clearly seen that there are _717748_ rows that have null value on its PUlocationID and DOlocationID.

## Question 4
Question: Best strategy to optimize the table if query always filter _pickup_datetime_ and order by _affiliated_base_number_. <br>
Answer:<br>
- Partition as same as filtering out data based on certain values. CLustering as same as ordering data alphabetically.
- If the query always filtering based on _pickup_datetime_ and ordering based on _affiliated_base_number, then the best strategy is do _partition by pickup_datetime_ and _cluster on affiliated_base_number_.

## Question 5
Question: Estimated bytes processed for query of retrieving distinct _affiliated_base_number_ between _pickup_datetime_ 2019/03/01 and 2019/03/31 on non-partitioned and partitioned tables.<br>
Logic:<br>
- Create new table from natural table that being partitioned by date of _pickup_datetime_ and clustered by affiliated_base_number.
- Take rows with distinct value of affiliated_base_number.
- Count total rows.

Query:<br>
- on Natural table
  ```sql
  SELECT COUNT(DISTINCT affiliated_base_number) AS distinct_number_of_affiliated_base_number_along_march_2019
  FROM `de-zoomcamp-375916.dezoomcamp.fhv_2019_natural`
  WHERE DATE(pickup_datetime) BETWEEN '2019-03-01' AND '2019-03-31';
  ```
- on Partitioned and Clustered table
  ```sql
  SELECT COUNT(DISTINCT affiliated_base_number) AS distinct_number_of_affiliated_base_number_along_march_2019
  FROM `de-zoomcamp-375916.dezoomcamp.fhv_2019_partitioned_clustered`
  WHERE DATE(pickup_datetime) BETWEEN '2019-03-01' AND '2019-03-31';
  ```
Result:<br>
- on Natural table
  ![image](https://user-images.githubusercontent.com/99194827/217857599-e6d50e1e-5c35-47a6-9095-45be4d9612b6.png)
- on Partitioned and Clustered table
  ![image](https://user-images.githubusercontent.com/99194827/217857833-28a6e520-8564-49b6-8a65-f69a48d35111.png)

From images above, it can be clearly seen that there are _647.87 MB_ and _23.05 MB_ data will be processed on natural and partitioned_and_clustered table, respectively.

## Question 6
Question: Place of data stored in External Table.<br>
Answer: GCP Bucket

## Question 7
Question: Best practice in BigQuery is by always clustering the data.<br>
Answer: False

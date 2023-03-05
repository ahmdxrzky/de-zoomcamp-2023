# Answer for Homework Week 5
Disclaimer: code script used to answer these questions is available [here](https://github.com/ahmdxrzky/de-zoomcamp-2023/blob/main/week5/homework.ipynb).

## Question 1
- Install Java, Spark, and PySpark by following this [installation guide](https://github.com/ahmdxrzky/de-zoomcamp-2023/blob/main/week5/installation_guide.md).
- Create a jupyter notebook (.ipynb) file.
- Import PySpark so it can be used in the notebook.
  ```python3
  from from pyspark.sql import SparkSession
  ```
- Create a local spark session by running this query below:
  ```python3
  spark = SparkSession.builder \
      .master("local[*]") \
      .appName('test') \
      .getOrCreate()
  ```
- Execute this to see what version of spark being used.
  ```python3
  spark.version
  ```
  
Result:
![image](https://user-images.githubusercontent.com/99194827/222944034-3dab97a8-bc92-4c9a-b7a0-831dcfc38975.png)
From image above, it can be clearly seen that version of spark being used is _3.3.2_.


## Question 2
- Download FHVHV trips data on June 2021 [here](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhvhv/fhvhv_tripdata_2021-06.csv.gz). It can be done via browser or terminal by execute command below:
  ```bash
  wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhvhv/fhvhv_tripdata_2021-06.csv.gz
  ```
- Extract the CSV file by execute command below:
  ```bash
  gunzip fhvhv_tripdata_2021-06.csv.gz
  ```
- Use pandas to see data type from each column of that csv file.
  ```python3
  import pandas as pd

  df_pd = pd.read_csv("fhvhv_tripdata_2021-06.csv")
  df_pd.dtypes
  ```
- See is any column has missing value.
  ```python3
  df_pd.isnull().sum()
  ```
  From this step, it can be seen that _Affiliated_base_number_ column has many missing values.
- Define schema for this table.
  ```python3
  from pyspark.sql import types

  schema = types.StructType([
      types.StructField('dispatching_base_num', types.StringType(), True),    # It's object file based on pandas dtypes
      types.StructField('pickup_datetime', types.TimestampType(), True),      # Datetime should be shown as timestamp data
      types.StructField('dropoff_datetime', types.TimestampType(), True),     # Datetime should be shown as timestamp data
      types.StructField('PULocationID', types.IntegerType(), True),           # It's integer file based on pandas dtypes
      types.StructField('DOLocationID', types.IntegerType(), True),           # It's integer file based on pandas dtypes
      types.StructField('SR_Flag', types.StringType(), True),                 # It's object file based on pandas dtypes
      types.StructField('Affiliated_base_number', types.StringType(), True)   # There are missing values here
  ])
  ```
- Read csv file with Spark.
  ```python3
  df = spark.read \
    .option("header", "true") \
    .schema(schema) \
    .csv('fhvhv_tripdata_2021-06.csv')
  ```
- Repartition this data into 12 parts.
  ```python3
  df = df.repartition(12)
  ```
- Write repartitioned data as parquet file.
  ```python3
  df.write \
    .parquet('fhvhv/2021/06', mode='overwrite')
  ```
- Find average value of parquet files size.
  ```
  import os
  import pathlib
  data = os.listdir('fhvhv/2021/06')
  datas = [doc for doc in data if doc[-3:] == "uet"]
  sizes = []

  for data in datas:
      size = os.path.getsize(pathlib.Path('fhvhv/2021/06/' + data).absolute())
      sizes.append(size)

  print(f'total size of parquet data on the folder: {sum(sizes)}')
  print(f'total parquet data on the folder: {len(sizes)}')
  print(f'average size per file: {(sum(sizes)/len(sizes))/1000000} MB')
  ```
  
Result:
![image](https://user-images.githubusercontent.com/99194827/222946687-d8f56142-cff2-439a-9c3b-3f588059aa36.png)
From image above, it can be clearly seen that average size of parquet files is _23.05 MB_ (choose 24 MB as it's the closest one).









Question:  <br>
Logic:  <br>
Query:
```
SELECT COUNT(1) AS total_fact_trips FROM `de-zoomcamp-375916.dbt_test.fact_trips`;
```
Result:
![image](https://user-images.githubusercontent.com/99194827/221353824-5a0156a3-11e9-45de-8a0d-adb74e617138.png)

From image above, it can be clearly seen that 

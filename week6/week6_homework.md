# Answer for Homework Week 6

## Install Kafka
Install Java and Kafka by following this [installation guide](https://github.com/ahmdxrzky/de-zoomcamp-2023/blob/main/week6/install_kafka.md).

## Download Dataset
Download [green taxi](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz) and [fhv](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_2019-01.csv.gz) trip data on January 2019 by executing command below:

```bash
https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz
https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_2019-01.csv.gz
```

Extract csv from those files by executing command below:

```bash
gunzip green_tripdata_2019-01.csv.gz
gunzip fhv_tripdata_2019-01.csv.gz
```

## Activate Kafka Zookeeper and Broker
Zookeeper and Broker are two important components of Kafka. Zookeeper takes role as "centralized manager" that manage all Brokers and ensure they work properly, while Broker takes role as "post officer" that manage data and ensure it stored well. Access a terminal and execute command below:
```bash
${KAFKA_HOME}/bin/zookeeper-server-start.sh ${KAFKA_HOME}/config/zookeeper.properties
```
Open another terminal and execute command below:
```bash
${KAFKA_HOME}/bin/kafka-server-start.sh ${KAFKA_HOME}/config/server.properties
```

## Ingest Data to Kafka Topics
In this case, define two kafka topics for each data source (csv file). Ingest data to those topics by executing [this file](https://github.com/ahmdxrzky/de-zoomcamp-2023/blob/main/week6/ingest_data.py) through another terminal with command below:
```bash
python3 ingest_data.py
```
What this file done explained as follows:
1. Create producer to send data to Kafka
2. Read green taxi csv file using Pandas
3. Send data row by row to Kafka Topics named green_trips (streamingly)
4. Do step 2 and 3 for fhv csv file to Kafka Topics named fhv_trips
5. Close producer after all of the data sent to Kafka


Execution time depends on infrastructure being used. I run kafka on my machine locally, so it takes around 2 hours and half to ingest all data to topics.

## Transform and Extract Data
Do some transformation as our expected result. Extract transformed data to PostgreSQL Database. All of this process run by executing [this file](https://github.com/ahmdxrzky/de-zoomcamp-2023/blob/main/week6/join_data.py) with command below:
```bash
python3 join_data.py
```
What this file done explained as follows:
1. Create consumer to access and read data from Kafka
2. Build PostgreSQL Connection
3. Do query to create an empty table named count_popularity (drop if exists and create)
4. Create buffer dictionary that contains counter for each location id
5. If the location id has already exists in database, we'll update counter data for that location id. Otherwise, we'll insert that location id as new data with counter equal 1

After this process, data will come to PostgreSQL Database streamingly.

## Query the Most Popular Location ID across Data
Because data has already sent to PostgreSQL Database, we can do query to see which is the most popular location id.
```sql
SELECT location_id AS most_popular_location_id
FROM count_popularity
ORDER BY count DESC
LIMIT 1;
```
Result:<br>
10:14 AM
![image](https://user-images.githubusercontent.com/99194827/224883830-272ea557-3450-4586-bf3b-a6240141945e.png)
10:15 AM
![image](https://user-images.githubusercontent.com/99194827/224883963-bbd07942-8be0-4619-a007-3ee39c631d53.png)

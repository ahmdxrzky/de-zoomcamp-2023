# Answer for Homework Week 1 Part A

## Number 1
Execute code below to see help documentation for command _docker build_: <br>
```docker build --help``` <br>
Result: <br>
![number1](https://user-images.githubusercontent.com/99194827/214724884-9f6e5e99-a66e-4f54-bce8-631647372dd5.png)
From image above, it can be clearly seen that tag ```--iidfile string``` can be used for _Write the image ID to the file_. <br>

## Number 2
Execute code below to run docker based on python:3.9 image in interactive mode and entrypoint bash: <br>
```
docker run -it --entrypoint=bash python:3.9
```
Then, execute code below to check modules installed on the container: <br>
```
pip list
```
Result: <br>
![number2](https://user-images.githubusercontent.com/99194827/214727087-0cf22a1a-35d4-483a-8ede-729ae2d3fd56.png)
From image above, it can be clearly seen that there are _already 3 modules being installed_ initially.

## Preparation
Before answering the rest of questions, inject _Green Taxi Trip on Jan 2019_ and _Taxi Zones_ data to PostgreSQL database running on a container. <br>
Build containers for PostgreSQL database and pgAdmin by executing [this docker-compose file](https://github.com/ahmdxrzky/de-zoomcamp-2023/blob/main/week1/docker-compose.yaml) with command below: <br>
```
docker-compose up -d
```
Executing [this python file](https://github.com/ahmdxrzky/de-zoomcamp-2023/blob/main/week1/ingest_zones.py) with command below to inject Taxi Zones data to PostgreSQL database: <br>
```
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"

python3 ingest_zones.py \
    --user=root \
    --password=root \
    --host=localhost \
    --port=5432 \
    --db=ny_taxi \
    --table_name=zones \
    --url=${URL}
```
Executing [this python file](https://github.com/ahmdxrzky/de-zoomcamp-2023/blob/main/week1/ingest_green_data.py) with command below to inject Green Taxi Trip on Jan 2019 data to PostgreSQL database: <br>
```
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz"

python3 ingest_green_data.py \
    --user=root \
    --password=root \
    --host=localhost \
    --port=5432 \
    --db=ny_taxi \
    --table_name=green_taxi_data_jan2019 \
    --url=${URL}
```
Those two python scripts above has already integrating 3 processes: <br>
1. Downloading csv or gz file from URL given.
2. If file downloaded in gz format, extracting the csv file from that gz file.
3. Injecting data from csv file to PostgreSQL database

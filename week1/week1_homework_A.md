# Answer for Homework Week 1 Part A

## Question 1
Execute command below to see help documentation for command _docker build_:
```
docker build --help
```
Result:
![number1](https://user-images.githubusercontent.com/99194827/214724884-9f6e5e99-a66e-4f54-bce8-631647372dd5.png)
From image above, it can be clearly seen that tag ```--iidfile string``` can be used for _Write the image ID to the file_.

## Question 2
Execute command below to run docker based on _python:3.9_ image in _interactive_ mode and entrypoint _bash_:
```
docker run -it --entrypoint=bash python:3.9
```
Then, execute command below to check modules installed on the container:
```
pip list
```
Result:
![number2](https://user-images.githubusercontent.com/99194827/214727087-0cf22a1a-35d4-483a-8ede-729ae2d3fd56.png)
From image above, it can be clearly seen that there are already _3 modules_ being installed at initial state.

## Preparation
Before answering the rest of questions, inject Green Taxi Trip on Jan 2019 and Taxi Zones data to PostgreSQL database running on a container. <br>
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
I do some edits, so those two python scripts above has already integrating 3 processes in a single execution: <br>
- Downloading csv or gz file from URL given.
- If file downloaded in gz format, extracting the csv file from that gz file.
- Injecting data from csv file to PostgreSQL database

Now, PostgreSQL database already has the data needed. Access and manipulate it through pgAdmin.

## Question 3
Question: Total taxi trips totally made on Jan 15th. <br>
Logic:
- Take row from data that has pickup and dropoff date equal to Jan 15th.
- Count how many rows fulfill criteria above.

Query:
```
SELECT
	COUNT(1) AS total_taxi_trips_on_jan_15
FROM
	public.green_taxi_data_jan2019
WHERE
	CAST(lpep_pickup_datetime AS DATE) = '2019-01-15' AND
	CAST(lpep_dropoff_datetime AS DATE) = '2019-01-15';
```
Result:
![number3](https://user-images.githubusercontent.com/99194827/214847767-0e47fdef-14b9-46ef-94cd-91899822ccaa.png)
From image above, it can be clearly seen that there are _20530_ taxi trips totally made on Jan 15th.

## Question 4
Question: Day with largest trip distance. <br>
Logic:
- Group data based on the pickup date.
- Take row with biggest trip distance for rows with same pickup date (aggregate).
- Order the data descendingly based on that aggregate result.
- Show only the first row of pickup date (has been ordered).

Query:
```
SELECT
	DATE(lpep_pickup_datetime) AS date_that_has_largest_trip_distance_value
FROM
	public.green_taxi_data_jan2019
GROUP BY
	DATE(lpep_pickup_datetime)
ORDER BY
	MAX(trip_distance) DESC
LIMIT
	1;
```
Result:
![number4](https://user-images.githubusercontent.com/99194827/214857205-b21726ef-7a99-4f3a-a3a9-16392c95007d.png)
From image above, it can be clearly seen that _Jan 15th, 2019_ has the largest trip distance compared to other dates.

## Question 5
Question: Trips with 2 and 3 passengers (respectively) on Jan 1st. <br>
Logic:
- Take row with the pickup, dropoff date, or both equal to Jan 1st.
- From result before, take row with 2 or 3 passengers, respectively.
- Count how many rows fulfill criterias above.

Query and Result for 2 passengers:
```
SELECT
	COUNT(1) AS trips_with_2_passengers_on_jan_1
FROM
	public.green_taxi_data_jan2019
WHERE
	(DATE(lpep_pickup_datetime) = '2019-01-01' OR
	 DATE(lpep_dropoff_datetime) = '2019-01-01') AND
	 passenger_count = 2;
```
![number5_2](https://user-images.githubusercontent.com/99194827/214861127-26d16f44-1fe8-4170-a540-abbfa95d236e.png)
Query and Result for 3 passengers:
```
SELECT
	COUNT(1) AS trips_with_3_passengers_on_jan_1
FROM
	public.green_taxi_data_jan2019
WHERE
	(DATE(lpep_pickup_datetime) = '2019-01-01' OR
	 DATE(lpep_dropoff_datetime) = '2019-01-01') AND
	 passenger_count = 3;
```
![image](https://user-images.githubusercontent.com/99194827/214861323-3541a1e4-6c01-4b6a-91ba-7fb7cea67f87.png)
From images above, it can be clearly seen that trips on Jan 1st with 2 and 3 passengers are _1282_ and _254_ trips, respectively.

## Question 6
Question: Name of drop off zone with largest tip with the passengers picked up in Astoria zone <br>
Logic:
- Join taxi trips table with zones table to retrieve name of pickup and dropoff zones.
- Take row with pickup zone equal to Astoria.
- Group data based on the dropoff zone.
- Take row with biggest tip amount for rows with same dropoff zone (aggregate).
- Order the data descendingly based on that aggregate result.
- Show only the first row of dropoff zone (has been ordered).

Query:
```
SELECT
	DOregion."Zone" AS drop_off_zone_that_had_largest_tip
FROM
	public.green_taxi_data_jan2019 AS trip
	JOIN public.zones AS PUregion
		ON trip."PULocationID" = PUregion."LocationID"
	JOIN public.zones AS DOregion
		ON trip."DOLocationID" = DOregion."LocationID"
WHERE
	PUregion."Zone" = 'Astoria'
GROUP BY
	DOregion."Zone"
ORDER BY
	MAX(trip.tip_amount) DESC
LIMIT
	1;
```
Result:
![image](https://user-images.githubusercontent.com/99194827/214863768-9054ef15-a3c7-4e08-b1b2-d8191770fd71.png)
From image above, it can be clearly seen that _Long Island City/Queen Plaza_ has the largest tip amount compared to other dropoff zones.

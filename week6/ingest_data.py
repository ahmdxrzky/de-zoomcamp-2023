from kafka import KafkaProducer
import pandas as pd
import time

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
start = time.time()

green_trips = pd.read_csv('green_tripdata_2019-01.csv')
for index, row in green_trips.iterrows():
    print(index, end=" ")
    producer.send('green_trips', value=row.to_json().encode('utf-8'))

print("\n")

fhv_trips = pd.read_csv('fhv_tripdata_2019-01.csv')
for index, row in fhv_trips.iterrows():
    print(index, end=" ")
    producer.send('fhv_trips', value=row.to_json().encode('utf-8'))

print(f"\nTotal time spent: {(time.time() - start) / 60} minutes = {(time.time() - start) / 60 / 60} hours")
producer.close()
from kafka import KafkaConsumer
import json
import psycopg2


topics = ['green_trips', 'fhv_trips']
consumer = KafkaConsumer(
    *topics,
    bootstrap_servers=['localhost:9092'],
    group_id='my-group',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

conn = psycopg2.connect(
    host="localhost",
    database="ny_taxi",
    user="root",
    password="root"
)
cur = conn.cursor()

sql = '''
    DROP TABLE count_popularity;
'''
cur.execute(sql)
conn.commit()
sql = '''
    CREATE TABLE IF NOT EXISTS count_popularity (
        location_id INT PRIMARY KEY,
        count INT NOT NULL
    );
'''
cur.execute(sql)
conn.commit()

buffer = {}
for message in consumer:
    try:
        record = message.value
        if message.topic == 'green_trips':
            if record['PULocationID'] in buffer.keys():
                buffer[record['PULocationID']] += 1
                data = tuple([buffer[record['PULocationID']], record['PULocationID']])
                sql = "UPDATE count_popularity SET count = %s WHERE location_id = %s;"
            else:
                buffer[record['PULocationID']] = 1
                data = tuple([record['PULocationID'], buffer[record['PULocationID']]])
                sql = "INSERT INTO count_popularity (location_id, count) VALUES (%s, %s);"
        else:
            if cur.fetchone() and record['PUlocationID'] in buffer.keys():
                buffer[record['PUlocationID']] += 1
                data = tuple([buffer[record['PUlocationID']], record['PUlocationID']])
                sql = "UPDATE count_popularity SET count = %s WHERE location_id = %s;"
            else:
                buffer[record['PUlocationID']] = 1
                data = tuple([record['PUlocationID'], buffer[record['PUlocationID']]])
                sql = "INSERT INTO count_popularity (location_id, count) VALUES (%s, %s);"
        cur.execute(sql, data)
        conn.commit()

        sql = """
            SELECT *
            FROM count_popularity
            ORDER BY count DESC
            LIMIT 1;
        """
        cur.execute(sql)
        cur.commit()

    except:
        continue

cur.close()
conn.close()
import os
# import argparse
from time import time
import pandas as pd
from sqlalchemy import create_engine
from prefect import flow, task
from prefect.tasks import task_input_hash
from prefect_sqlalchemy import SqlAlchemyConnector
from datetime import timedelta

@task(log_prints=True, retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def extract_data(url):
    gz_name = f'output.csv.gz'

    os.system(f"wget {url} -O {gz_name}")
    os.system(f"gunzip {gz_name}")

    df_iter = pd.read_csv(gz_name[:-3], iterator=True, chunksize=100000)
    df = next(df_iter)
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    return df

@task(log_prints=True)
def transform_data(df):
    print(f"pre:missing passenger count: {df['passenger_count'].isin([0]).sum()}")
    df = df[df['passenger_count'] != 0]
    print(f"post:missing passenger count: {df['passenger_count'].isin([0]).sum()}")
    return df

@task(log_prints=True, retries=3)
def ingest_data(table_name, df):
    connection_block = SqlAlchemyConnector.load("postgres-connector")

    with connection_block.get_connection(begin=False) as engine:
        df.head(0).to_sql(name=table_name, con=engine, if_exists='replace')
        df.to_sql(name=table_name, con=engine, if_exists='append')

@flow(name="Subflow", log_prints=True)
def log_subflow(table_name: str):
    print(f"Logging Subflow for: {table_name}")

@flow(name="Ingest Flow")
def main(table_name: str):
    url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"
    log_subflow(table_name)
    raw = extract_data(url)
    preprop = transform_data(raw)
    ingest_data(table_name, preprop)

if __name__ == "__main__":
    main("yellow_taxi_data_jan2021")
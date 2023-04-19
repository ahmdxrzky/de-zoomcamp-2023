import os
import argparse
from time import time
import pandas as pd
from sqlalchemy import create_engine

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    gz_name = f'{table_name}_output.csv.gz'

    os.system(f"wget {url} -O {gz_name}")
    os.system(f"gunzip {gz_name}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df_iter = pd.read_csv(gz_name[:-3], iterator=True, chunksize=100000)
    df = next(df_iter)
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    df.head(0).to_sql(name=table_name, con=engine, if_exists='replace')
    df.to_sql(name=table_name, con=engine, if_exists='append')

    try:
        while True:
            start = time()

            df = next(df_iter)
            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
            df.to_sql(name=table_name, con=engine, if_exists='append')

            print(f'inserted another chunk, took {round(time() - start, 3)} second')
        
    except StopIteration:
        print("All data has been inserted.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres database.')
    
    parser.add_argument('--user', help='username for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of the table for the results')
    parser.add_argument('--url', help='url of the csv file')

    args = parser.parse_args()

    main(args)
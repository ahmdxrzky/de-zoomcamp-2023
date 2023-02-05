import os
from pathlib import Path
import pandas as pd
from typing import Tuple
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket


@task(retries=3)
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read taxi data from web into pandas DataFrame"""
    df = pd.read_csv(dataset_url)
    return df

@task(log_prints=True)
# edit starts here
def clean(df: pd.DataFrame, color: str) -> Tuple[pd.DataFrame, str]:
    # edit ends here
    """Fix dtype issues"""
    #edit starts here
    if color == "green":
        df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])
        df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'])
    elif color == "yellow":
        df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
        df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
    #edit ends here
    print(df.head(2))
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    # edit starts here
    return df, len(df)
    # edit ends here

@task()
def write_local(df_clean: pd.DataFrame, color: str, dataset_file: str) -> Path:
    """Write DataFrame out locally as parquet file"""
    path = Path(f'data/{color}/{dataset_file}.parquet')
    #edit starts here
    os.makedirs(path.absolute().parent, exist_ok=True)
    #edit ends here
    df_clean.to_parquet(path, compression="gzip")
    return path

@task()
def write_gcs(path: Path) -> None:
    """Upload local parquet file to GCS"""
    gcs_block = GcsBucket.load("gcs-bucket")
    gcs_block.upload_from_path(
        from_path=path,
        to_path=path
    )
    return

@flow()
def etl_web_to_gcs(
    # edit starts here
    color: str = "green",
    year: int = 2020,
    month: int = 1
) -> int:
    """"The main ETL function"""
    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"

    df = fetch(dataset_url)
    df_clean, total = clean(df, color)
    path = write_local(df_clean, color, dataset_file)
    write_gcs(path)
    return total
    # edit ends here

if __name__ == "__main__":
    etl_web_to_gcs()

import os
import sys
import time
import pandas as pd
from pathlib import Path
from datetime import datetime
from prefect import flow, task
from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket

@task()
def fetch_from_source(url: str) -> pd.DataFrame:
    """Download dataset from source"""
    df = pd.read_csv(url, index_col=0)
    df.reset_index(inplace=True)
    return df

@task()
def write_parquet_local(df: pd.DataFrame, year: int, month: int) -> Path:
    """Write DataFrame out locally as parquet file"""
    gcs_path = Path(os.path.join("data", str(year), f"{year}_{month:02}.parquet"))
    local_path = Path(os.path.join(Path(__file__).absolute().parent, "upload", gcs_path))
    if not os.path.exists(local_path.parent):
        os.system(f"mkdir -p {local_path.parent}")
    df.to_parquet(local_path, index=False)
    return local_path, gcs_path

@task()
def write_parquet_gcs(local_path: Path, gcs_path: Path) -> None:
    """Upload local parquet file to GCS"""
    gcs_block = GcsBucket.load("gcs-bucket-final-project")
    gcs_block.upload_from_path(
        from_path=local_path,
        to_path=gcs_path
    )
    return

@task()
def extract_from_gcs(year: int, month: int) -> Path:
    """Download trip data from GCS"""
    gcs_path = Path(os.path.join("data", str(year), f"{year}_{month:02}.parquet"))
    local_path = Path(os.path.join(Path(__file__).absolute().parent, "download", gcs_path))
    gcs_block = GcsBucket.load("gcs-bucket-final-project")
    if not os.path.exists(local_path.parent):
        os.system(f"mkdir -p {local_path.parent}")
    gcs_block.get_directory(from_path = gcs_path, local_path = local_path)
    return local_path

@task()
def read_dataframe(path: Path) -> pd.DataFrame:
    df = pd.read_parquet(path)
    return df

@task()
def write_to_gbq(df: pd.DataFrame) -> None:
    """Write DataFrame to BigQuery"""
    gcp_credentials = GcpCredentials.load("gcp-credentials-final-project")
    df.to_gbq(
        destination_table="final_project.all_weather_data",
        project_id="de-zoomcamp-375916",
        credentials=gcp_credentials.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append"
    )
    return

@flow(log_prints=True)
def etl_monthly(year: int, month: int) -> None:
    """ETL function per month"""
    url = f"https://raw.githubusercontent.com/ahmdxrzky/de-zoomcamp-2023/main/final_project/assets/dataset/{year}/{year}_{month:02}.csv"
    df = fetch_from_source(url)
    local_path, gcs_path = write_parquet_local(df, year, month)
    write_parquet_gcs(local_path, gcs_path)
    local_path = extract_from_gcs(year, month)
    df = read_dataframe(local_path)
    write_to_gbq(df)
    
    return 

@flow(log_prints=True)
def etl_total(initial: bool = False, years: list = list(range(2015, 2023)), months: list = list(range(1, 13))) -> None:
    """"The main ETL function"""
    if initial == True:
        for year in years:
            for month in months:
                etl_monthly(year, month)
        etl_monthly(2023, 1)
    else:
        current_datetime = datetime.fromtimestamp(time.time())
        current_year = current_datetime.year
        current_month = current_datetime.month - 1
        etl_monthly(current_year, current_month)
    return

if __name__ == "__main__":
    try:
        arg1 = sys.argv[1]
        etl_total(initial = arg1)
    except:
        etl_total()

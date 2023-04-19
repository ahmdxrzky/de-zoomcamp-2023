import os
import time
import pandas as pd
from pathlib import Path
from datetime import datetime
from prefect import flow, task
from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket

@task()
def extract_from_source(url: str) -> pd.DataFrame:
    """
    Download dataset from source.
    
    :param url: (str) URL of data source.
    :return: (pandas.DataFrame) Dataframe of data from data source.
    """
    df = pd.read_csv(url, index_col=0)
    df.reset_index(inplace=True)
    return df

@task()
def write_parquet_to_local(df: pd.DataFrame, year: int, month: int) -> tuple([Path, Path]):
    """
    Write DataFrame as parquet file in local directory.
    
    :param df: (pandas.DataFrame) Dataframe that will be exported as parquet file.
    :param year: (int) Year of data will be processed.
    :param month: (int) Month of data will be processed.
    :return: (Path) Path to parquet file on local directory.
    :return: (Path) Path to parquet file on data lake.
    """
    gcs_path = Path(os.path.join("data", str(year), f"{year}_{month:02}.parquet"))
    local_path = Path(os.path.join(Path(__file__).absolute().parent, "upload", gcs_path))
    if not os.path.exists(local_path.parent):
        os.system(f"mkdir -p {local_path.parent}")
    df.to_parquet(local_path, index=False)
    return local_path, gcs_path

@task()
def write_parquet_to_gcs(local_path: Path, gcs_path: Path) -> None:
    """
    Upload local parquet file to GCS.

    :param local_path: (Path) Path to parquet file on local directory that being uploaded to data lake.
    :param gcs_path: (Path) Path to parquet file on data lake.
    """
    gcs_block = GcsBucket.load("gcs-bucket-final-project")
    gcs_block.upload_from_path(
        from_path=local_path,
        to_path=gcs_path,
        timeout=5000
    )
    return

@task()
def extract_from_gcs(year: int, month: int) -> Path:
    """
    Download data from GCS.
    
    :param year: (int) Year of data will be processed.
    :param month: (int) Month of data will be processed.
    :return: (Path) Path to downloaded parquet file on local directory.
    """
    gcs_path = Path(os.path.join("data", str(year), f"{year}_{month:02}.parquet"))
    local_path = Path(os.path.join(Path(__file__).absolute().parent, "download", gcs_path))
    gcs_block = GcsBucket.load("gcs-bucket-final-project")
    if not os.path.exists(local_path.parent):
        os.system(f"mkdir -p {local_path.parent}")
    gcs_block.get_directory(from_path = gcs_path, local_path = local_path)
    return local_path

@task()
def read_parquet_as_dataframe(path: Path) -> pd.DataFrame:
    """
    Read parquet file as dataframe.

    :param path: (Path) Path of downloaded parquet file.
    :return: (pandas.DataFrame) Dataframe from parquet file.
    """
    df = pd.read_parquet(path)
    return df

@task()
def write_dataframe_to_gbq(df: pd.DataFrame) -> None:
    """
    Write DataFrame to BigQuery table.
    
    :param df: (pandas.DataFrame) Dataframe that will be ingested to BigQuery table.
    """
    gcp_credentials = GcpCredentials.load("gcp-credentials-final-project")
    df.to_gbq(
        destination_table="final_project.all_weather_data",
        project_id=os.environ.get("PROJECT_ID"),
        credentials=gcp_credentials.get_credentials_from_service_account(),
        if_exists="append"
    )
    return

@flow(log_prints=True)
def etl_ingest_to_data_lake(url: str, year: int, month: int) -> None:
    """
    ETL process from data source to data lake.

    :param url: (str) URL of data source.
    :param year: (int) Year of data will be processed.
    :param month: (int) Month of data will be processed.
    """
    df = extract_from_source(url)
    local_path, gcs_path = write_parquet_to_local(df, year, month)
    write_parquet_to_gcs(local_path, gcs_path)
    return

@flow(log_prints=True)
def etl_ingest_to_data_warehouse(year: int, month: int) -> None:
    """
    ETL process from data lake to data warehouse.

    :param year: (int) Year of data will be processed.
    :param month: (int) Month of data will be processed.
    """
    local_path = extract_from_gcs(year, month)
    df = read_parquet_as_dataframe(local_path)
    write_dataframe_to_gbq(df)

@flow(log_prints=True)
def etl_for_a_month(year: int, month: int) -> None:
    """
    ETL function for a month.
    
    :param year: (int) Year of data will be processed.
    :param month: (int) Month of data will be processed.
    """
    url = f"https://raw.githubusercontent.com/ahmdxrzky/de-zoomcamp-2023/main/final_project/assets/dataset/{year}/{year}_{month:02}.csv"
    etl_ingest_to_data_lake(url, year, month)
    etl_ingest_to_data_warehouse(year, month)
    return 

@flow(log_prints=True)
def etl_main_function(
    initial: bool = False,
    years: list = list(range(2015, 2023)),
    months: list = list(range(1, 13))
) -> None:
    """"
    The main function for all ETL process.
    
    :param initial: (bool)
        If it sets as True, it means ETL process is ingesting initial dataset (2015 to Jan 2023).
        If it sets as False, it means ETL process is ingesting batch data (start with data from February 2023 that should be run with Deployment on Mar 1st, 2023).
    :param years: (list) Years of all data available.
    :param months: (list) Months in number.
    """
    current_datetime = datetime.fromtimestamp(time.time())
    current_year = current_datetime.year
    current_month = current_datetime.month

    if initial == True:
        for year in years:
            for month in months:
                etl_for_a_month(year, month)
        for month in range(1, current_month):
            etl_for_a_month(2023, month)
    else:
        current_month -= 1
        etl_for_a_month(current_year, current_month)
    return

if __name__ == "__main__":
    etl_main_function()

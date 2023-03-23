import os
import sys
import time
import pandas as pd
from pathlib import Path
from datetime import datetime
from prefect import flow, task
from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket


@task(retries=3)
def extract_from_gcs(year: int, month: int) -> Path:
    """Download trip data from GCS"""
    gcs_path = Path(os.path.join("data", str(year), f"{year}_{month:02}.parquet"))
    local_path = Path(os.path.join(Path(__file__).absolute().parent, "data", "download", gcs_path))
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

@flow()
def etl_gcs_to_bq(year: int, month: int) -> Path:
    """Parameterized ETL function to load data into BigQuery"""
    path = extract_from_gcs(year, month)
    df = read_dataframe(path)
    write_to_gbq(df)
    return path

@flow(log_prints=True)
def etl_monthly(initial: bool = False, years: list = list(range(2011, 2023)), months: list = list(range(1, 13))) -> None:
    """Main ETL function"""
    if initial == True:
        for year in years:
            for month in months:
                path = etl_gcs_to_bq(year, month)
                print(f"Load {path} successfully.")
        path = etl_gcs_to_bq(2023, 1)
        print(f"Load {path} successfully.")
    else:
        current_datetime = datetime.fromtimestamp(time.time())
        current_year = current_datetime.year
        current_month = current_datetime.month - 1
        path = etl_gcs_to_bq(current_year, current_month)
        print(f"Load {path} successfully.")
    
if __name__ == "__main__":
    try:
        arg1 = sys.argv[1]
        etl_monthly(initial = arg1)
    except:
        etl_monthly()
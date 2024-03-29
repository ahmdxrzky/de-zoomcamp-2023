import os
from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials


@task(retries=3)
def extract_from_gcs(color: str, year: int, month: int) -> Path:
    """Download trip data from GCS"""
    gcs_path = f"data/{color}/{color}_tripdata_{year}-{month:02}.parquet"
    gcs_block = GcsBucket.load("gcs-bucket")
    # edit starts here
    gcs_block.get_directory(from_path = gcs_path, local_path = os.path.join("data", "download"))
    return Path(os.path.join("data", "download", gcs_path))
    # edit ends here

@task()
def write_bq(df: pd.DataFrame) -> int:
    """Write DataFrame to BigQuery"""
    gcp_credentials = GcpCredentials.load("gcp-creds")

    df.to_gbq(
        # edit starts here
        destination_table="dezoomcamp.yellow_rides",
        project_id="de-zoomcamp-375916",
        # edit ends here
        credentials=gcp_credentials.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append"
    )

    # edit starts here
    return len(df)
    # edit ends here

@flow()
def etl_gcs_to_bq(
    color: str,
    year: int,
    month: int
) -> int:
    """Parameterized ETL function to load data into BigQuery"""
    path = extract_from_gcs(color, year, month)
    df = pd.read_parquet(path)
    total = write_bq(df)
    # edit starts here
    return total
    # edit ends here

# edit starts here
@flow(log_prints=True)
# edit ends here
def etl_main_flow(
    # edit starts here
    color: str = "yellow",
    year: int = 2019,
    months: list = [2, 3]
    # edit ends here
) -> None:
    """Main ETL function"""
    total_rows = 0
    for month in months:
        total_rows += etl_gcs_to_bq(color, year, month)
    print(f"total rows of migrated data: {total_rows}")

if __name__ == "__main__":
    color = "yellow"
    year = 2019
    months = [2, 3]
    etl_main_flow(color, year, months)
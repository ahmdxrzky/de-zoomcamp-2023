import os
from pathlib import Path
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket


@task(retries=3)
def write_local(
    dataset_url: str,
    dataset_title: str
) -> Path:
    """Download gz file from web"""
    path = Path(f'data/{dataset_url.split("/")[-2]}/{dataset_title}.csv.gz')
    os.makedirs(path.absolute().parent, exist_ok=True)
    os.system(f"wget {dataset_url} -O {path}")
    return path

@task(retries=3)
def write_gcs(path: Path) -> None:
    """Upload local gz file to GCS"""
    gcs_block = GcsBucket.load("gcs-bucket")
    gcs_block.upload_from_path(
        from_path=path,
        to_path=path,
        timeout=500000000
    )
    return

@flow(log_prints=True)
def etl_month(
    color: str = "fhv",
    year: int = 2019,
    month: int = 1
) -> None:
    """"ETL function for file for each month"""
    dataset_title = f"{color}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_title}.csv.gz"

    path = write_local(dataset_url, dataset_title)
    write_gcs(path)
    print(f"Success for {month}")

@flow(log_prints=True)
def etl_year(
    color: str = "fhv",
    year: int = 2019,
    months: list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
) -> None:
    """Main ETL function"""
    for month in months:
        etl_month(color, year, month)

if __name__ == "__main__":
    etl_year()

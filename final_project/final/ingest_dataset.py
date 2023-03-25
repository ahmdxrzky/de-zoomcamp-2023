import os
import pandas as pd
from pathlib import Path
from prefect import flow, task
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

@flow(log_prints=True)
def etl_source_per_month(year: int, month: int) -> None:
    """ETL function per month"""
    url = f"https://raw.githubusercontent.com/ahmdxrzky/de-zoomcamp-2023/main/final_project/assets/dataset/{year}/{year}_{month:02}.csv"
    df = fetch_from_source(url)
    local_path, gcs_path = write_parquet_local(df, year, month)
    write_parquet_gcs(local_path, gcs_path)
    return

@flow(log_prints=True)
def etl_source_to_gcs() -> None:
    """"The main ETL function"""
    for year in range(2011, 2024):
        for month in range(1, 13):
            etl_source_per_month(year, month)
    return

if __name__ == "__main__":
    etl_source_to_gcs()
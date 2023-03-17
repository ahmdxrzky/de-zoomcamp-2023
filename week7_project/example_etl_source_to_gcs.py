from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket


@task(retries=3)
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read taxi data from local file into pandas DataFrame"""
    df = pd.read_csv(dataset_url)
    return df

@task()
def write_local(df_clean: pd.DataFrame, color: str, dataset_file: str) -> Path:
    """Write DataFrame out locally as parquet file"""
    path = Path(f'../data/{color}/{dataset_file}.parquet')
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
def etl_web_to_gcs() -> None:
    """"The main ETL function"""
    df = fetch("weatherAUS.csv")
    df_clean = clean(df)
    path = write_local(df_clean, color, dataset_file)
    write_gcs(path)

if __name__ == "__main__":
    etl_web_to_gcs()
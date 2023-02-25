import os
import pyarrow
from google.cloud import storage
import time

"""
Pre-reqs: 
1. `pip install pandas pyarrow google-cloud-storage`
2. Set environment variable GOOGLE_APPLICATION_CREDENTIALS to your project/service-account key
3. Set environment variable GCP_GCS_BUCKET as your bucket or change default value of BUCKET
"""

# services = ['fhv','green','yellow']
init_url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/'
# switch out the bucketname
BUCKET = os.environ.get("GCP_GCS_BUCKET", "dtc-data-lake-bucketname")


def download_gz(
    request_url: str,
    service: str,
    file_name: str
) -> None:
    """Download gz file from web"""
    os.makedirs(f"data_csv/{service}", exist_ok=True)
    os.system(f"wget {request_url} -O data_csv/{service}/{file_name}.gz")


def upload_to_gcs(
    bucket: str,
    object_name: str,
    local_file: str
) -> None:
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    
    Upload local file to GCS
    """
    client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file, timeout=50000)


def web_to_gcs(
    year: str,
    service: str
) -> None:
    """Main ETL process for each services per year"""
    for i in range(12):
        
        # sets the month part of the file_name string
        month = '0'+str(i+1)
        month = month[-2:]

        # download gz file
        file_name = service + '_tripdata_' + year + '-' + month + '.csv'
        request_url = init_url + service + "/" + file_name + ".gz"
        download_gz(request_url, service, file_name)
        print(f"Local: data_csv/{service}/{file_name}.gz")

        # upload it to gcs 
        upload_to_gcs(BUCKET, f"data/{service}/{file_name}", os.path.join("data_csv", service, file_name + ".gz"))
        print(f"GCS: data/{service}/{file_name}.gz")


if __name__ == "__main__":
    web_to_gcs('2019', 'green')
    time.sleep(10)
    web_to_gcs('2020', 'green')
    time.sleep(10)
    web_to_gcs('2019', 'yellow')
    time.sleep(10)
    web_to_gcs('2020', 'yellow')
    time.sleep(10)
    web_to_gcs('2019', 'fhv')

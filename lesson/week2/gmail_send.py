from prefect import flow
from prefect_email import EmailServerCredentials, email_send_message
from etl_web_to_gcs import etl_web_to_gcs


email_credentials_block = EmailServerCredentials.load("gmail-creds")

@flow(log_prints=True)
def send_email() -> None:
    """Send email when ETL process done"""
    total = etl_web_to_gcs(year=2019, month=4)
    message = f"{total} data has been ingested to Google Cloud Storage"
    print(message)

    email_send_message(
        email_server_credentials=email_credentials_block,
        subject="Update from Prefect Flow",
        msg=message,
        email_to=dict(email_credentials_block)['username'],
    )
    return

if __name__ == "__main__":
    send_email()
from pathlib import Path

import pandas as pd
from prefect import flow, task
from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket


@task(retries=3)
def extract_from_gcs(color: str, year: int, month: int) -> Path:
    """Download trip data from GCS"""
    gcs_path = f"data/{color}/{color}_tripdata_{year}-{month:02}.parquet"
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.get_directory(from_path=gcs_path, local_path=f"./data/")
    return Path(f"./data/{gcs_path}")


@task()
def transform(path: Path) -> pd.DataFrame:
    """Data cleaning example"""
    df = pd.read_parquet(path)
    print(f"pre: missing passenger count: {df['passenger_count'].isna().sum()}")
    df["passenger_count"].fillna(0, inplace=True)
    print(f"post: missing passenger count: {df['passenger_count'].isna().sum()}")
    return df


@task()
def write_bq(df: pd.DataFrame) -> None:
    """Write DataFrame to BiqQuery"""
    chunk_size = 100_000
    gcp_credentials_block = GcpCredentials.load("account")

    for i in range(0, df.shape[0], chunk_size):
        df[i:i+chunk_size].to_gbq(
            destination_table="dezoomcamp.rides",
            project_id="dtc-de-375513",
            credentials=gcp_credentials_block.get_credentials_from_service_account(),
            if_exists="append",
        )
        print(f'Finish batch {(i // chunk_size) + 1}')


@flow(log_prints=True)
def etl_gcs_to_bq(color, year, months):
    """Main ETL flow to load data into Big Query"""
    for month in months:
        path = extract_from_gcs(color, year, month)
        df = pd.read_parquet(path)
        print(f'Num of rows: {df.shape[0]}')
        # df = transform(path)
        write_bq(df)


if __name__ == "__main__":
    etl_gcs_to_bq("yellow", 2019, [2, 3])

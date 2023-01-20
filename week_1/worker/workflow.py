import gzip
import os
import re
import shutil
import tempfile

import pandas as pd
import requests
from prefect import flow, task
from sqlalchemy import create_engine
from tqdm import tqdm


def download(url: str, destination: str):
    filename = url.split('/')[-1]
    filepath = os.path.join(destination, filename)

    with requests.get(url, stream=True) as stream:
        total_size_in_bytes = int(stream.headers.get('Content-Length', 0))
        block_size_in_bytes = 1024
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        with open(filepath, 'wb') as file:
            for chunk in stream.iter_content(block_size_in_bytes):
                progress_bar.set_description(f'Downloading {filename}...')
                progress_bar.update(len(chunk))
                file.write(chunk)
        progress_bar.close()

    return filepath


@task
def connect_to_pg():
    url = 'postgresql://root:root@postgres:5432/dtc'
    return create_engine(url)


@task
def create_tmp_dir():
    return tempfile.mkdtemp()


@task
def remove_tmp_dir(tmp_dir: str):
    shutil.rmtree(tmp_dir)


@task
def download_green_taxi_file(destination: str):
    url = f'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/' \
          f'green_tripdata_2019-01.csv.gz'
    green_taxi_file_path = download(url, destination)
    return green_taxi_file_path


@task
def download_taxi_zone_lookup_file(destination: str):
    url = f'https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv'
    taxi_zone_lookup_file_path = download(url, destination)
    return taxi_zone_lookup_file_path


@task
def ingest_green_taxi_data(file_path, pg_con):
    extracted_file_path = re.match(
        r'(?P<extracted_file_path>.*).gz',
        file_path
    ).group('extracted_file_path')

    print(f'Extracting {file_path} into {extracted_file_path}...')
    with gzip.open(file_path, 'rb') as file_in:
        with open(extracted_file_path, 'wb') as file_out:
            for line in file_in:
                file_out.write(line)

    print(f'Transforming date type in {file_path}...')
    df_iter = pd.read_csv(
        extracted_file_path,
        parse_dates=['lpep_pickup_datetime', 'lpep_dropoff_datetime'],
        iterator=True,
        chunksize=10_000
    )

    print(f'Loading transformed data into Postgres (might take time, please patient!)...')
    for df in df_iter:
        df.to_sql(
            schema='public',
            name='green_taxi',
            con=pg_con,
            index=False,
            if_exists='append'
        )


@task
def ingest_taxi_zone_lookup_data(file_path, pg_con):
    df = pd.read_csv(file_path)
    df.to_sql(
        schema='public',
        name='taxi_zone_lookup',
        con=pg_con,
        index=False,
        if_exists='append'
    )


@flow(name="Ingest taxi data into Postgres")
def run_workflow():
    download_dir = create_tmp_dir()
    green_taxi_file_path = download_green_taxi_file(download_dir)
    taxi_zone_lookup_file_path = download_taxi_zone_lookup_file(download_dir)
    pg_con = connect_to_pg()
    ingest_green_taxi_data(green_taxi_file_path, pg_con)
    ingest_taxi_zone_lookup_data(taxi_zone_lookup_file_path, pg_con)
    remove_tmp_dir(download_dir)


run_workflow()

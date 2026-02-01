#!/usr/bin/env python
# coding: utf-8

import pyarrow.parquet as pq
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm
import click

dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}


def ingest_data(
        url: str,
        engine,
        target_table: str,
        chunksize: int = 100000,
) -> None:
    parquet_file = pd.read_parquet(url)

    total_rows = len(parquet_file)

    # Create table with first chunk
    first_chunk = parquet_file.iloc[:chunksize]
    first_chunk.to_sql(
        name=target_table,
        con=engine,
        if_exists="replace"
    )

    print(f"Table {target_table} created")
    print(f"Inserted first chunk: {len(first_chunk)}")

    # Insert remaining chunks
    for start in tqdm(range(chunksize, total_rows, chunksize)):
        end = min(start + chunksize, total_rows)
        df_chunk = parquet_file.iloc[start:end]
        df_chunk.to_sql(
            name=target_table,
            con=engine,
            if_exists="append"
        )
        print(f"Inserted chunk: {len(df_chunk)}")

    print(f'Done ingesting {total_rows} rows to {target_table}')


@click.command()
@click.option("--pg-user", default="root", help="Postgres user")
@click.option("--pg-pass", "pg_pass", default="root", help="Postgres password")
@click.option("--pg-host", default="localhost", help="Postgres host")
@click.option("--pg-port", default="5432", help="Postgres port")
@click.option("--pg-db", default="ny_taxi", help="Postgres database name")
@click.option("--year", default=2021, type=int, help="Year of the taxi data")
@click.option("--month", default=1, type=int, help="Month of the taxi data")
@click.option("--chunksize", default=100000, type=int, help="Chunksize for insertion")
@click.option("--target-table", "target_table", default="yellow_taxi_data", help="Target table name")
def main(pg_user, pg_pass, pg_host, pg_port, pg_db, year, month, chunksize, target_table):
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
    # url_prefix = 'https://d37ci6vzurychx.cloudfront.net/trip-data'
    #
    # url = f'{url_prefix}/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    url = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet"

    ingest_data(
        url=url,
        engine=engine,
        target_table=target_table,
        chunksize=chunksize
    )


if __name__ == '__main__':
    main()
#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine
import click

dtype = {
    "index": "Int64",
    "LocationID": "Int64",
    "Borough": "string",
    "Zone": "string",
    "service_zone": "string"
}

def ingest_data(
        url: str,
        engine
) -> None:
    df = pd.read_csv(
        url,
        dtype=dtype
    )

    df.to_sql(
        name='zones_green',
        con=engine,
        if_exists="replace"
    )

    print(f"Inserted {len(df)} rows to 'zones'")


@click.command()
@click.option("--pg-user", default="root", help="Postgres user")
@click.option("--pg-pass", "pg_pass", default="root", help="Postgres password")
@click.option("--pg-host", default="localhost", help="Postgres host")
@click.option("--pg-port", default="5432", help="Postgres port")
@click.option("--pg-db", default="ny_taxi", help="Postgres database name")
def main(pg_user, pg_pass, pg_host, pg_port, pg_db):
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
    url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv'

    ingest_data(
        url=url,
        engine=engine
    )


if __name__ == '__main__':
    main()
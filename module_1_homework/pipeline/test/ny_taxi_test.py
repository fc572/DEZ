import pytest
import psycopg2
from psycopg2.extras import RealDictCursor

@pytest.fixture(scope="module")
def db_connection():
    # Replace with your Docker Postgres credentials
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="ny_taxi",
        user="root",
        password="root"
    )
    yield conn
    conn.close()

@pytest.fixture(scope="module")
def cursor(db_connection):
    cur = db_connection.cursor(cursor_factory=RealDictCursor)
    yield cur
    cur.close()

def test_row_count(cursor):
    cursor.execute("SELECT COUNT(*) FROM yellow_taxi_trips_2021_2")
    count = cursor.fetchone()['count']
    assert count > 0  # Basic check

def test_row_count_specific(cursor):
    cursor.execute("SELECT COUNT(*) FROM yellow_taxi_trips_2021_2")
    count = cursor.fetchone()['count']
    assert count == 1371708  # Strict check if source size is known

#    /*** Connect to the database and find the name of the table to connect to.
#     Start to take notes for all this commandas */
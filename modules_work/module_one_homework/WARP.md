# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is the Data Engineer Zoomcamp (DEZ) repository, focused on building data pipelines for ingesting NYC taxi data into PostgreSQL. The project uses Python with modern tooling (uv for package management) and Docker for infrastructure.

## Technology Stack

- **Python**: 3.12+ (managed via `.python-version`)
- **Package Manager**: `uv` (modern, fast Python package manager)
- **Database**: PostgreSQL 18 (via Docker)
- **Admin UI**: pgAdmin 4 (via Docker)
- **Key Libraries**: pandas, SQLAlchemy, psycopg2, pyarrow, click

## Project Structure

```
DEZ/
├── pipeline/              # Main pipeline code
│   ├── ingest_data.py    # Data ingestion script with CLI
│   ├── pipeline.py       # Sample pipeline script
│   ├── main.py           # Basic entry point
│   ├── test/             # Test directory
│   │   └── ny_taxi_test.py  # Database tests
│   ├── pyproject.toml    # Python dependencies
│   ├── uv.lock           # Locked dependencies
│   ├── docker-compose.yaml  # DB infrastructure
│   └── Dockerfile        # Container for data ingestion
```

## Common Commands

### Dependency Management (uv)

All dependency commands should be run from the `pipeline/` directory:

```bash
# Install dependencies (creates .venv if needed)
uv sync

# Install with dev dependencies
uv sync --dev

# Add a new dependency
uv add <package-name>

# Add a dev dependency
uv add --dev <package-name>

# Run a command in the uv environment
uv run python <script.py>
```

### Database Infrastructure

```bash
# Start PostgreSQL and pgAdmin containers
docker compose -f pipeline/docker-compose.yaml up -d

# Stop containers
docker compose -f pipeline/docker-compose.yaml down

# View logs
docker compose -f pipeline/docker-compose.yaml logs -f

# Stop and remove volumes (clears all data)
docker compose -f pipeline/docker-compose.yaml down -v
```

**Database Connection Info:**
- PostgreSQL: `localhost:5432`
  - User: `root`
  - Password: `root`
  - Database: `ny_taxi`
- pgAdmin: `http://localhost:8085`
  - Email: `admin@admin.com`
  - Password: `root`

### Running Data Ingestion

The `ingest_data.py` script downloads NYC taxi data and loads it into PostgreSQL:

```bash
# Basic ingestion (defaults to 2021-01)
uv run python pipeline/ingest_data.py

# Specify year and month
uv run python pipeline/ingest_data.py --year 2021 --month 2

# Full options
uv run python pipeline/ingest_data.py \
  --pg-user root \
  --pg-pass root \
  --pg-host localhost \
  --pg-port 5432 \
  --pg-db ny_taxi \
  --year 2021 \
  --month 1 \
  --chunksize 100000 \
  --target-table yellow_taxi_data
```

### Running Tests

```bash
# Run all tests (requires database to be running)
uv run pytest pipeline/test/

# Run specific test file
uv run pytest pipeline/test/ny_taxi_test.py

# Run with verbose output
uv run pytest -v pipeline/test/
```

**Note**: Tests expect the database to be running and populated with data from 2021-02.

### Interactive Database Access

```bash
# Using pgcli (dev dependency)
uv run pgcli -h localhost -p 5432 -U root -d ny_taxi

# Using standard psql (if installed)
psql -h localhost -p 5432 -U root -d ny_taxi
```

### Jupyter Notebooks

```bash
# Start Jupyter (dev dependency)
uv run jupyter notebook
```

## Architecture & Data Flow

### Data Ingestion Pattern

The `ingest_data.py` script implements a chunked CSV ingestion pattern:

1. **Download**: Fetches compressed CSV from GitHub (NYC TLC data releases)
2. **Schema Creation**: Creates table structure from first chunk (empty DataFrame)
3. **Chunked Loading**: Streams data in configurable chunks (default 100k rows) to handle large files
4. **Type Safety**: Enforces specific dtypes for taxi data fields (see `dtype` dict in `ingest_data.py`)

Key implementation details:
- Uses pandas `iterator=True` with `chunksize` for memory efficiency
- SQLAlchemy for database connections
- tqdm for progress tracking
- Click for CLI argument parsing

### Docker Container Pattern

The Dockerfile demonstrates a multi-stage build with uv:
- Base: Python 3.13-slim
- Copies uv binary from official uv image
- Installs dependencies using `uv sync --locked` for reproducibility
- Sets up virtual environment in `/app/.venv`

### Database Schema

NYC Yellow Taxi data includes:
- Trip timestamps (`tpep_pickup_datetime`, `tpep_dropoff_datetime`)
- Location IDs (`PULocationID`, `DOLocationID`)
- Payment info (`fare_amount`, `tip_amount`, `total_amount`, etc.)
- Trip metadata (`passenger_count`, `trip_distance`, `RatecodeID`, etc.)

## Development Notes

### Testing Strategy

Tests use pytest with direct psycopg2 connections (not SQLAlchemy) and `RealDictCursor` for dictionary-style row access. Tests verify:
- Row count validation
- Specific table data integrity

### Output Files

The repository ignores `*.parquet` files (see `.gitignore`), as `pipeline.py` generates parquet output files during execution.

### Python Version

The project is pinned to Python 3.12+ via `.python-version`. The Docker image uses 3.13.10-slim but the project dependencies require `>=3.12`.

# dlt-practice

Practice project for learning [dlt](https://dlthub.com/) (data load tool) — building Python data pipelines that extract from a source and load into a destination.

## What's here

- **`main.py`** — Minimal pipeline that loads the `family` and `genome` tables from a SQL database into a local DuckDB file, using incremental loading on `family` and full-replace on `genome`.
- **`sql_database_pipeline.py`** — Additional SQL-database source examples and pipeline patterns.
- **`.dlt/config.toml`** — dlt configuration. Secrets live in `.dlt/secrets.toml`, which is gitignored.

## Requirements

- Python >= 3.14
- [uv](https://docs.astral.sh/uv/) for dependency management

## Setup

```bash
# Install dependencies into a virtual environment
uv sync
```

Add your source database credentials to `.dlt/secrets.toml` (this file is gitignored):

```toml
[sources.sql_database.credentials]
drivername = "mysql+pymysql"
database = "your_db"
username = "your_user"
password = "your_password"
host = "your_host"
port = 3306
```

## Run

```bash
uv run python main.py
```

This produces a local `sql_to_duckdb_pipeline.duckdb` file (gitignored) containing the loaded data.

## Notes

`secrets.toml` and `*.duckdb` files are excluded from version control via `.gitignore`.

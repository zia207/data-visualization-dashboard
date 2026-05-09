# SQL Engine Benchmark Dashboard

A Streamlit dashboard that benchmarks **PySpark, DuckDB, Dask-SQL, SQLAlchemy, psycopg2, and Polars** against the NYS Tax dataset (or any CSV/Parquet you upload).

## Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Features

| Tab | What you get |
|-----|-------------|
| ⚡ Benchmark | Run any SQL across selected engines, see latency bar chart, leaderboard, result previews |
| 🗂 Data Preview | Filter, sort, and explore the dataset; numeric histograms |
| 🔬 Schema & Stats | Column types, null %, descriptive stats, correlation heatmap |
| 📖 Engine Guide | Install commands, pros/cons, and a decision guide |

## Sidebar Options

- **Data source** — built-in NYS Tax sample (10k–200k rows) or upload your own CSV/Parquet
- **Engines** — tick any combination to benchmark
- **Query templates** — choose a preset or write custom SQL (`{table}` is the placeholder)
- **Runs per engine** — average over N runs for stable timing

## Engine Requirements

| Engine | Install | Extra |
|--------|---------|-------|
| DuckDB | `pip install duckdb` | — |
| Polars | `pip install polars` | — |
| SQLAlchemy | `pip install sqlalchemy` | — (uses SQLite in-memory) |
| psycopg2 | `pip install psycopg2-binary` | Running PostgreSQL instance |
| PySpark | `pip install pyspark` | Java 11+ |
| Dask-SQL | `pip install dask[dataframe] dask-sql` | — |

Engines that aren't installed are gracefully skipped and shown as **Not Installed** in results.

## Using Your Own Data

Upload any CSV or Parquet file via the sidebar. Column names are auto-detected and shown in the query editor hint. Use `{table}` in your SQL — it maps to your file's table.

## NYS Tax Columns (built-in sample)

| Column | Description |
|--------|-------------|
| Tax_Year | 2019–2023 |
| County | 20 NYS counties |
| NY_AGI_FDAP | Adjusted Gross Income |
| Tax_Liability_Status | Filing category |
| Filing_Status | Single / Married / etc. |
| Num_Exemptions | 0–7 |
| Tax_Before_Credits | Tax liability pre-credit |
| STAR_Credit | School Tax Relief credit |
| Child_Credit | Child tax credit amount |
| Net_Tax_Due | Final tax owed |

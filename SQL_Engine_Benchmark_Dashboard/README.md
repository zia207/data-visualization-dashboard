# SQL Engine Benchmark Dashboard

A Streamlit dashboard that benchmarks **PySpark, DuckDB, Dask-SQL, SQLAlchemy, psycopg2, and Polars** against built-in **Yellow Taxi** or **NYS Tax** samples (or any CSV/Parquet you upload).

## Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open **http://localhost:8501**.

## Static webpage (LBC-style)

| Path | Purpose |
|------|---------|
| **`web/index.html`** | Landing page: overview, links to the static demo & main site, “Run locally”. |
| **`web/css/styles.css`**, **`web/js/main.js`**, **`web/assets/favicon.svg`** | Same layout pattern as the repo root `web/` site (soft theme). |

GitHub Pages publishes this folder as **`/sql_engine_benchmark/`** (see root `README.md`). The interactive chart-only preview lives at the repo root as **`sql_engine_benchmark.html`**.

## Features

| Tab | What you get |
|-----|-------------|
| ⚡ Benchmark | Template / custom SQL across engines, leaderboard, “how to fix” hints |
| 📊 Query & Visualize | Single engine, results table, Plotly charts |
| 🗂 Data Preview | Filter, sort, explore; numeric histograms |
| 🔬 Schema & Stats | dtypes, null %, describe, correlation heatmap |
| 📖 Engine Guide | installs, pros/cons, picking an engine |

## Sidebar Options

- **Data source** — Yellow Taxi sample, NYS Tax sample, or upload CSV/Parquet + optional taxi zone lookup CSV for joins
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

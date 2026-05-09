import streamlit as st
import pandas as pd
import numpy as np
import time
import random
import io
import traceback
from datetime import datetime

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SQL Engine Benchmark Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}
code, pre, .stCode {
    font-family: 'JetBrains Mono', monospace !important;
}

/* Soft theme — warm paper, muted pastels */
.stApp {
    background-color: #f5f3f0;
    color: #3d3a45;
}

.main .block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

/* Header */
.dash-header {
    background: linear-gradient(135deg, #faf8f6 0%, #f3efe9 50%, #faf8f6 100%);
    border-bottom: 1px solid #ebe8e4;
    padding: 1.5rem 0 1rem 0;
    margin-bottom: 1.5rem;
    border-radius: 0 0 12px 12px;
}
.dash-title {
    font-size: 2.4rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    background: linear-gradient(90deg, #9b8fd4, #d4a5c7, #8ec8c0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
}
.dash-subtitle {
    color: #8b8798;
    font-size: 0.95rem;
    margin-top: 0.4rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* Metric cards */
.metric-card {
    background: #ffffff;
    border: 1px solid #ebe8e4;
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s, box-shadow 0.2s;
    box-shadow: 0 1px 3px rgba(61, 58, 69, 0.06);
}
.metric-card:hover { border-color: #c9c2db; box-shadow: 0 4px 12px rgba(155, 143, 212, 0.12); }
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #9b8fd4, #b8dfd7);
}
.metric-label {
    color: #8b8798;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.3rem;
}
.metric-value {
    font-size: 2rem;
    font-weight: 800;
    color: #3d3a45;
    font-family: 'JetBrains Mono', monospace;
    line-height: 1;
}
.metric-unit {
    font-size: 0.85rem;
    color: #8b8798;
    margin-left: 0.3rem;
}
.metric-delta {
    font-size: 0.8rem;
    margin-top: 0.4rem;
}
.delta-good { color: #5d9b7a; }
.delta-bad  { color: #d48484; }

/* Engine badge */
.engine-badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    font-family: 'JetBrains Mono', monospace;
}

/* Section headers */
.section-header {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: #8b8798;
    border-bottom: 1px solid #ebe8e4;
    padding-bottom: 0.5rem;
    margin-bottom: 1rem;
    font-weight: 600;
}

/* Result table */
.stDataFrame { background: #ffffff !important; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #efede9 !important;
    border-right: 1px solid #e5e2de;
}
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: #7a6eb0;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
}

/* Status pills */
.status-ok   { color: #5d9b7a; }
.status-warn { color: #c9a227; }
.status-err  { color: #d48484; }
.status-skip { color: #8b8798; }

/* Code block */
.query-box {
    background: #faf8f6;
    border: 1px solid #ebe8e4;
    border-left: 3px solid #9b8fd4;
    border-radius: 8px;
    padding: 1rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: #5c5280;
    white-space: pre-wrap;
    overflow-x: auto;
}

/* Log */
.log-box {
    background: #faf8f6;
    border: 1px solid #ebe8e4;
    border-radius: 8px;
    padding: 0.8rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #8b8798;
    max-height: 260px;
    overflow-y: auto;
}
.log-ok   { color: #5d9b7a; }
.log-err  { color: #d48484; }
.log-info { color: #6b9fc9; }
.log-warn { color: #c9a227; }

/* Progress bar override */
.stProgress > div > div > div { background: linear-gradient(90deg, #9b8fd4, #b8dfd7) !important; }

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #e8e4f4, #ddefee);
    border: 1px solid #c9c2db;
    color: #3d3a45;
    font-family: 'Syne', sans-serif;
    font-weight: 600;
    letter-spacing: 0.05em;
    border-radius: 8px;
    padding: 0.5rem 1.5rem;
    transition: all 0.2s;
}
.stButton > button:hover {
    border-color: #9b8fd4;
    background: linear-gradient(135deg, #ddd5f0, #cee8e4);
}

/* Selectbox, multiselect */
.stSelectbox label, .stMultiSelect label, .stSlider label, .stCheckbox label {
    color: #6f6a7a !important;
    font-size: 0.8rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: transparent;
    border-bottom: 1px solid #ebe8e4;
    gap: 0;
}
.stTabs [data-baseweb="tab"] {
    color: #8b8798 !important;
    font-family: 'Syne', sans-serif;
    font-size: 0.82rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding: 0.5rem 1.2rem;
    border-bottom: 2px solid transparent;
}
.stTabs [aria-selected="true"] {
    color: #6f5fb8 !important;
    border-bottom: 2px solid #9b8fd4 !important;
    background: transparent !important;
}
</style>
""", unsafe_allow_html=True)

# ── Engine Definitions ──────────────────────────────────────────────────────────
ENGINES = {
    "PySpark": {
        "color": "#f97316",
        "bg": "#f9731622",
        "icon": "🔥",
        "pkg": "pyspark",
        "description": "Apache Spark SQL — distributed queries for large or cluster data; JVM startup adds local overhead.",
    },
    "DuckDB": {
        "color": "#facc15",
        "bg": "#facc1522",
        "icon": "🦆",
        "pkg": "duckdb",
        "description": "Embedded OLAP engine — very fast analytical SQL on DataFrames, CSV, and Parquet; no server.",
    },
    "Dask-SQL": {
        "color": "#a78bfa",
        "bg": "#a78bfa22",
        "icon": "⚙️",
        "pkg": "dask_sql",
        "description": "SQL on Dask DataFrames — parallel, out-of-core pandas-style workloads across cores.",
    },
    "SQLAlchemy": {
        "color": "#34d399",
        "bg": "#34d39922",
        "icon": "🔗",
        "pkg": "sqlalchemy",
        "description": "Python SQL toolkit — this dashboard uses in-memory SQLite; same patterns work for Postgres/MySQL.",
    },
    "psycopg2": {
        "color": "#60a5fa",
        "bg": "#60a5fa22",
        "icon": "🐘",
        "pkg": "psycopg2",
        "description": "PostgreSQL adapter — native wire protocol; here it needs a running Postgres instance to execute.",
    },
    "Polars": {
        "color": "#f43f5e",
        "bg": "#f43f5e22",
        "icon": "🐻‍❄️",
        "pkg": "polars",
        "description": "Polars SQL — Rust DataFrame engine with a SQL context; strong speed and memory efficiency.",
    },
}

# Taxi-style templates use strftime / epoch math so SQLite (SQLAlchemy) matches DuckDB-style usage.
TAXI_QUERY_TEMPLATES = {
    "DateTime: Extract Hour and Count Trips":
        "SELECT CAST(strftime('%H', tpep_pickup_datetime) AS INTEGER) AS pickup_hour,\n       COUNT(*) AS trip_count\nFROM {table}\nGROUP BY pickup_hour\nORDER BY pickup_hour",
    "DateTime: Daily Trips (strftime day)":
        "SELECT strftime('%Y-%m-%d', tpep_pickup_datetime) AS trip_date,\n       COUNT(*) AS trip_count,\n       ROUND(SUM(total_amount), 2) AS daily_revenue\nFROM {table}\nGROUP BY trip_date\nORDER BY trip_date",
    "DateTime: Formatted Pickup Timestamp":
        "SELECT strftime('%Y-%m-%d %H:%M', tpep_pickup_datetime) AS pickup_minute,\n       fare_amount,\n       total_amount\nFROM {table}\nLIMIT 50",
    "DateTime: Trip Duration in Minutes":
        "SELECT tpep_pickup_datetime,\n       tpep_dropoff_datetime,\n"
        "       (CAST(strftime('%s', tpep_dropoff_datetime) AS REAL)\n"
        "        - CAST(strftime('%s', tpep_pickup_datetime) AS REAL)) / 60.0 AS duration_min\n"
        "FROM {table}\nWHERE tpep_dropoff_datetime IS NOT NULL\n  AND tpep_pickup_datetime IS NOT NULL\nLIMIT 100",

    "Agg: Payment Type Summary":
        "SELECT COALESCE(payment_type, 'Unknown') AS payment_type,\n       COUNT(*) AS trip_count,\n       ROUND(AVG(fare_amount), 2) AS avg_fare,\n       ROUND(SUM(total_amount), 2) AS total_revenue\nFROM {table}\nGROUP BY COALESCE(payment_type, 'Unknown')\nORDER BY trip_count DESC",
    "Agg: Distinct Vendors + Stats":
        "SELECT COUNT(*) AS total_trips,\n       COUNT(DISTINCT vendor_id) AS unique_vendors,\n       ROUND(AVG(trip_distance), 2) AS avg_trip_distance,\n       MIN(passenger_count) AS min_passengers,\n       MAX(passenger_count) AS max_passengers\nFROM {table}",
    "Agg: Revenue per Mile (Safe Division)":
        "SELECT ROUND(SUM(total_amount) / NULLIF(SUM(trip_distance), 0), 4) AS revenue_per_mile,\n       ROUND(SUM(total_amount), 2) AS total_revenue,\n       ROUND(SUM(trip_distance), 2) AS total_distance\nFROM {table}\nWHERE trip_distance > 0",

    "Cleaning: Tip Flag with CASE WHEN":
        "SELECT CASE WHEN tip_amount > 0 THEN 'Tipped' ELSE 'No Tip' END AS tip_flag,\n       COUNT(*) AS trip_count,\n       ROUND(AVG(tip_amount), 2) AS avg_tip\nFROM {table}\nGROUP BY CASE WHEN tip_amount > 0 THEN 'Tipped' ELSE 'No Tip' END\nORDER BY trip_count DESC",
    "Cleaning: Outlier Filter + Clamp Fare":
        "SELECT payment_type,\n       ROUND(AVG(GREATEST(fare_amount, 0)), 2) AS avg_non_negative_fare,\n       ROUND(AVG(trip_distance), 2) AS avg_distance,\n       COUNT(*) AS trip_count\nFROM {table}\nWHERE trip_distance BETWEEN 0.1 AND 50.0\n  AND fare_amount > 0\nGROUP BY payment_type\nORDER BY trip_count DESC",

    "Join: Borough-Level Aggregation":
        "SELECT z.Borough,\n       COUNT(*) AS trip_count,\n       ROUND(AVG(t.total_amount), 2) AS avg_total_amount,\n       ROUND(SUM(t.total_amount), 2) AS total_revenue\nFROM {table} t\nJOIN {lookup_table} z ON t.PULocationID = z.LocationID\nGROUP BY z.Borough\nORDER BY trip_count DESC",

    "Window: Top 3 Longest Trips per Payment Type":
        "SELECT payment_type, trip_distance, total_amount\nFROM (\n    SELECT payment_type,\n           trip_distance,\n           total_amount,\n           ROW_NUMBER() OVER (PARTITION BY payment_type ORDER BY trip_distance DESC) AS rn\n    FROM {table}\n) ranked\nWHERE rn <= 3\nORDER BY payment_type, trip_distance DESC",
    "Window: Rank Top Pickup Zones by Revenue":
        "SELECT PULocationID,\n       daily_revenue,\n       RANK() OVER (ORDER BY daily_revenue DESC) AS revenue_rank\nFROM (\n    SELECT PULocationID, ROUND(SUM(total_amount), 2) AS daily_revenue\n    FROM {table}\n    GROUP BY PULocationID\n) zone_rev\nORDER BY revenue_rank\nLIMIT 20",
    "Window: Running Daily Revenue":
        "SELECT trip_day,\n       pickup_ts,\n       total_amount,\n"
        "       SUM(total_amount) OVER (\n           PARTITION BY trip_day\n           ORDER BY pickup_ts\n       ) AS running_daily_rev\n"
        "FROM (\n    SELECT strftime('%Y-%m-%d', tpep_pickup_datetime) AS trip_day,\n"
        "           tpep_pickup_datetime AS pickup_ts,\n           total_amount\n    FROM {table}\n) x\n"
        "ORDER BY trip_day, pickup_ts\nLIMIT 200",
    "Window: Quartile Fare Analysis":
        "SELECT fare_amount,\n       NTILE(4) OVER (ORDER BY fare_amount) AS fare_quartile\nFROM {table}\nWHERE fare_amount > 0\nLIMIT 200",
    "Custom SQL": "",
}

NYS_QUERY_TEMPLATES = {
    "Count Records":
        "SELECT COUNT(*) AS total_records\nFROM {table}",
    "Top Counties by Gross Income":
        "SELECT \"County\", SUM(\"NY_AGI_FDAP\") AS total_agi\nFROM {table}\nGROUP BY \"County\"\nORDER BY total_agi DESC\nLIMIT 10",
    "Income Bracket Distribution":
        "SELECT \"Tax_Liability_Status\", COUNT(*) AS cnt,\n       AVG(\"NY_AGI_FDAP\") AS avg_agi\nFROM {table}\nGROUP BY \"Tax_Liability_Status\"",
    "Null Audit":
        "SELECT COUNT(*) AS total,\n       COUNT(\"County\") AS has_county,\n       COUNT(\"NY_AGI_FDAP\") AS has_agi\nFROM {table}",
    "Custom SQL": "",
}


def query_templates_for(data_source: str) -> dict:
    if data_source == "NYS Tax Sample (built-in)":
        return NYS_QUERY_TEMPLATES
    return TAXI_QUERY_TEMPLATES


# ── Sample data generator ───────────────────────────────────────────────────────
@st.cache_data
def load_nys_sample(n_rows: int = 50_000) -> pd.DataFrame:
    """Generate synthetic NYS Tax-like data."""
    rng = np.random.default_rng(42)
    counties = [
        "Albany","Bronx","Brooklyn","Buffalo","Chautauqua","Erie",
        "Kings","Manhattan","Nassau","New York","Niagara","Oneida",
        "Onondaga","Orange","Queens","Richmond","Rockland","Suffolk",
        "Ulster","Westchester",
    ]
    brackets = ["No Tax Liability","Tax Liability","Refund Only","Part-Year","Non-Resident"]
    filing   = ["Single","Married Joint","Married Separate","Head of Household"]

    df = pd.DataFrame({
        "Tax_Year":            rng.choice([2019,2020,2021,2022,2023], n_rows),
        "County":              rng.choice(counties, n_rows),
        "NY_AGI_FDAP":         rng.lognormal(11, 1.2, n_rows).round(2),
        "Tax_Liability_Status":rng.choice(brackets, n_rows),
        "Filing_Status":       rng.choice(filing, n_rows),
        "Num_Exemptions":      rng.integers(0, 8, n_rows),
        "Tax_Before_Credits":  rng.lognormal(9, 1.5, n_rows).round(2),
        "STAR_Credit":         rng.choice([0,0,0,500,1000,1500], n_rows, p=[.55,.15,.1,.1,.05,.05]),
        "Child_Credit":        rng.choice([0,500,1000,2000], n_rows, p=[.5,.2,.2,.1]),
        "Net_Tax_Due":         rng.lognormal(8, 1.8, n_rows).round(2),
    })
    return df


@st.cache_data
def load_yellow_taxi_sample(n_rows: int = 50_000) -> pd.DataFrame:
    """Synthetic NYC yellow-taxi-style rows for built-in templates (joins need zone CSV upload)."""
    rng = np.random.default_rng(43)
    base = pd.Timestamp("2024-06-01")
    pickup_offset = pd.to_timedelta(rng.uniform(0, 30 * 24 * 3600, n_rows), unit="s")
    pickups = base + pickup_offset
    trip_sec = rng.integers(120, 7200, n_rows)
    dropoffs = pickups + pd.to_timedelta(trip_sec, unit="s")

    trip_distance = rng.lognormal(1.0, 0.8, n_rows).clip(0.1, 50.0).round(2)
    fare_amount = (trip_distance * rng.uniform(2.5, 5.0, n_rows) + rng.uniform(2.0, 8.0, n_rows)).round(2)
    tip_amount = np.where(rng.random(n_rows) > 0.45, rng.uniform(0, 8.0, n_rows).round(2), 0.0)
    total_amount = (fare_amount + tip_amount + rng.choice([0, 0.5, 1.0], n_rows)).round(2)

    payment_type = rng.choice(["1", "2", "3", "4", "5"], n_rows, p=[0.58, 0.18, 0.12, 0.07, 0.05])
    vendor_id = rng.choice([1, 2], n_rows, p=[0.55, 0.45])
    passenger_count = rng.integers(1, 7, n_rows)
    pulocation_id = rng.integers(1, 264, n_rows)

    return pd.DataFrame({
        "tpep_pickup_datetime": pickups,
        "tpep_dropoff_datetime": dropoffs,
        "trip_distance": trip_distance,
        "fare_amount": fare_amount,
        "tip_amount": tip_amount,
        "total_amount": total_amount,
        "payment_type": payment_type,
        "vendor_id": vendor_id,
        "passenger_count": passenger_count,
        "PULocationID": pulocation_id,
    })


# ── Engine runners ──────────────────────────────────────────────────────────────
def format_sql_query(sql: str, main_table: str, lookup_table: str = "taxi_zone_lookup") -> str:
    """Replace SQL placeholders used by query templates."""
    return sql.replace("{table}", main_table).replace("{lookup_table}", lookup_table)

def run_duckdb(
    df: pd.DataFrame,
    sql: str,
    main_table: str = "nys_tax",
    lookup_df: pd.DataFrame | None = None,
    lookup_table: str = "taxi_zone_lookup",
) -> tuple[pd.DataFrame, float, str]:
    try:
        import duckdb
        t0 = time.perf_counter()
        con = duckdb.connect()
        con.register(main_table, df)
        if lookup_df is not None and not lookup_df.empty:
            con.register(lookup_table, lookup_df)
        result = con.execute(format_sql_query(sql, main_table, lookup_table)).df()
        elapsed = time.perf_counter() - t0
        return result, elapsed, "ok"
    except ImportError:
        return pd.DataFrame(), 0, "not_installed"
    except Exception as e:
        return pd.DataFrame(), 0, str(e)

def run_polars(
    df: pd.DataFrame,
    sql: str,
    main_table: str = "nys_tax",
    lookup_df: pd.DataFrame | None = None,
    lookup_table: str = "taxi_zone_lookup",
) -> tuple[pd.DataFrame, float, str]:
    try:
        import polars as pl
        t0 = time.perf_counter()
        ldf = pl.from_pandas(df).lazy()
        ctx_tables = {main_table: ldf}
        if lookup_df is not None and not lookup_df.empty:
            ctx_tables[lookup_table] = pl.from_pandas(lookup_df).lazy()
        ctx = pl.SQLContext(**ctx_tables, eager=True)
        result = ctx.execute(format_sql_query(sql, main_table, lookup_table)).to_pandas()
        elapsed = time.perf_counter() - t0
        return result, elapsed, "ok"
    except ImportError:
        return pd.DataFrame(), 0, "not_installed"
    except Exception as e:
        return pd.DataFrame(), 0, str(e)

def run_sqlalchemy(
    df: pd.DataFrame,
    sql: str,
    main_table: str = "nys_tax",
    lookup_df: pd.DataFrame | None = None,
    lookup_table: str = "taxi_zone_lookup",
) -> tuple[pd.DataFrame, float, str]:
    try:
        from sqlalchemy import create_engine, text
        t0 = time.perf_counter()
        engine = create_engine("sqlite:///:memory:", future=True)
        df.to_sql(main_table, engine, index=False, if_exists="replace")
        if lookup_df is not None and not lookup_df.empty:
            lookup_df.to_sql(lookup_table, engine, index=False, if_exists="replace")
        with engine.connect() as con:
            result = pd.read_sql(text(format_sql_query(sql, main_table, lookup_table)), con)
        elapsed = time.perf_counter() - t0
        return result, elapsed, "ok"
    except ImportError:
        return pd.DataFrame(), 0, "not_installed"
    except Exception as e:
        return pd.DataFrame(), 0, str(e)

def run_psycopg2(
    df: pd.DataFrame,
    sql: str,
    main_table: str = "nys_tax",
    lookup_df: pd.DataFrame | None = None,
    lookup_table: str = "taxi_zone_lookup",
) -> tuple[pd.DataFrame, float, str]:
    try:
        import psycopg2
        return pd.DataFrame(), 0, "requires_postgres"
    except ImportError:
        return pd.DataFrame(), 0, "not_installed"

def run_pyspark(
    df: pd.DataFrame,
    sql: str,
    main_table: str = "nys_tax",
    lookup_df: pd.DataFrame | None = None,
    lookup_table: str = "taxi_zone_lookup",
) -> tuple[pd.DataFrame, float, str]:
    try:
        from pyspark.sql import SparkSession
        t0 = time.perf_counter()
        spark = (SparkSession.builder
                 .master("local[*]")
                 .appName("BenchDash")
                 .config("spark.ui.showConsoleProgress", "false")
                 .getOrCreate())
        spark.sparkContext.setLogLevel("ERROR")
        sdf = spark.createDataFrame(df)
        sdf.createOrReplaceTempView(main_table)
        if lookup_df is not None and not lookup_df.empty:
            spark.createDataFrame(lookup_df).createOrReplaceTempView(lookup_table)
        result = spark.sql(format_sql_query(sql, main_table, lookup_table)).toPandas()
        elapsed = time.perf_counter() - t0
        return result, elapsed, "ok"
    except ImportError:
        return pd.DataFrame(), 0, "not_installed"
    except Exception as e:
        return pd.DataFrame(), 0, str(e)

def run_dask_sql(
    df: pd.DataFrame,
    sql: str,
    main_table: str = "nys_tax",
    lookup_df: pd.DataFrame | None = None,
    lookup_table: str = "taxi_zone_lookup",
) -> tuple[pd.DataFrame, float, str]:
    try:
        import dask.dataframe as dd
        from dask_sql import Context
        t0 = time.perf_counter()
        ddf = dd.from_pandas(df, npartitions=4)
        ctx = Context()
        ctx.create_table(main_table, ddf)
        if lookup_df is not None and not lookup_df.empty:
            lookup_ddf = dd.from_pandas(lookup_df, npartitions=1)
            ctx.create_table(lookup_table, lookup_ddf)
        result = ctx.sql(format_sql_query(sql, main_table, lookup_table)).compute()
        elapsed = time.perf_counter() - t0
        return result, elapsed, "ok"
    except ImportError:
        return pd.DataFrame(), 0, "not_installed"
    except Exception as e:
        return pd.DataFrame(), 0, str(e)

ENGINE_RUNNERS = {
    "DuckDB":     run_duckdb,
    "Polars":     run_polars,
    "SQLAlchemy": run_sqlalchemy,
    "psycopg2":   run_psycopg2,
    "PySpark":    run_pyspark,
    "Dask-SQL":   run_dask_sql,
}

STATUS_LABELS = {
    "ok":               ("✓ OK",           "status-ok"),
    "not_installed":    ("✗ Not Installed", "status-skip"),
    "requires_postgres":("⚠ Needs Postgres","status-warn"),
    "skip":             ("– Skipped",       "status-skip"),
}

def status_html(code: str) -> str:
    label, css = STATUS_LABELS.get(code, (f"✗ {code[:20]}", "status-err"))
    return f'<span class="{css}">{label}</span>'

def status_fix_hint(code: str) -> str:
    hints = {
        "ok": "No action needed.",
        "skip": "Engine was skipped in this run.",
        "not_installed": "Install engine package in this environment (see requirements).",
        "requires_postgres": "Configure and run a PostgreSQL server, then provide connection settings.",
    }
    if code in hints:
        return hints[code]
    if "JAVA_GATEWAY_EXITED" in code:
        return "Install Java 11+ and verify JAVA_HOME for the Streamlit process."
    low = code.lower()
    if "not found in from clause" in low or "referenced column" in low or "unable to find column" in low:
        return (
            'Use **Yellow Taxi Sample** with taxi templates, or **NYS Tax** with tax templates — '
            "or align your uploaded columns with the SQL (see Available columns)."
        )
    if "near \"from\": syntax error" in low and "extract" in low:
        return (
            "SQLAlchemy uses SQLite (no `EXTRACT(...)` like Postgres). "
            "Use taxi templates with `strftime`, or run the query in DuckDB/Polars."
        )
    if "syntax error" in low and "sqlite" in low:
        return "Check SQL dialect: SQLAlchemy path is SQLite; prefer strftime-based templates or DuckDB."
    return "Review the error text, dataset columns, and engine SQL dialect (SQLite vs DuckDB/Polars)."

def engine_badge(name: str) -> str:
    cfg = ENGINES[name]
    return (f'<span class="engine-badge" '
            f'style="background:{cfg["bg"]};color:{cfg["color"]};'
            f'border:1px solid {cfg["color"]}55;">'
            f'{cfg["icon"]} {name}</span>')

def apply_soft_plotly_layout(fig, height: int | None = None):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Syne", color="#3d3a45"),
        margin=dict(l=0, r=0, t=30, b=10),
    )
    fig.update_xaxes(gridcolor="#ebe8e4", color="#8b8798")
    fig.update_yaxes(gridcolor="#ebe8e4", color="#8b8798")
    if height is not None:
        fig.update_layout(height=height)

def infer_viz_defaults(res_df: pd.DataFrame) -> tuple[str, str | None, str | None]:
    """Return (kind, x_col, y_col) for Auto mode."""
    if res_df.empty or len(res_df.columns) == 0:
        return "table", None, None
    num_cols = res_df.select_dtypes(include=[np.number]).columns.tolist()
    non_num = [c for c in res_df.columns if c not in num_cols]
    if non_num and num_cols:
        return "bar", non_num[0], num_cols[0]
    if len(num_cols) >= 2:
        return "scatter", num_cols[0], num_cols[1]
    if len(num_cols) == 1:
        return "histogram", num_cols[0], None
    return "table", None, None

def map_ui_chart_to_kind(ui: str, inferred: tuple[str, str | None, str | None]) -> tuple[str, str | None, str | None]:
    auto_k, auto_x, auto_y = inferred
    if ui == "Auto":
        return auto_k, auto_x, auto_y
    if ui == "Bar chart":
        return "bar", None, None
    if ui == "Line chart":
        return "line", None, None
    if ui == "Scatter plot":
        return "scatter", None, None
    if ui == "Histogram":
        return "histogram", None, None
    return "table", None, None

def render_query_output_chart(
    res_df: pd.DataFrame,
    kind: str,
    x_col: str | None,
    y_col: str | None,
    accent: str,
):
    if res_df.empty:
        st.info("No rows to visualize.")
        return
    try:
        import plotly.express as px
    except ImportError:
        st.info("Install plotly for charts: `pip install plotly`")
        return

    if kind == "table" or kind == "none":
        return

    try:
        if kind == "histogram" and x_col:
            fig = px.histogram(res_df, x=x_col, color_discrete_sequence=[accent])
            fig.update_traces(marker_line_width=0)
        elif kind == "bar" and x_col and y_col:
            fig = px.bar(res_df, x=x_col, y=y_col, color_discrete_sequence=[accent])
        elif kind == "line" and x_col and y_col:
            fig = px.line(
                res_df, x=x_col, y=y_col,
                color_discrete_sequence=[accent], markers=True,
            )
        elif kind == "scatter" and x_col and y_col:
            fig = px.scatter(res_df, x=x_col, y=y_col, color_discrete_sequence=[accent])
        else:
            st.caption("Pick chart columns that match the selected chart type.")
            return
        apply_soft_plotly_layout(fig, height=420)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.warning(f"Could not build chart: {e}")

# ── Sidebar ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚡ Configuration")
    st.divider()

    st.markdown("### Dataset")
    data_source = st.radio(
        "Source",
        [
            "Yellow Taxi Sample (built-in)",
            "NYS Tax Sample (built-in)",
            "Upload CSV / Parquet",
        ],
        label_visibility="collapsed",
    )

    uploaded_df = None
    lookup_df = None
    if data_source == "NYS Tax Sample (built-in)":
        table_name = "nys_tax"
    else:
        table_name = "trips"
    lookup_table_name = "taxi_zone_lookup"

    if data_source == "Upload CSV / Parquet":
        up = st.file_uploader("Upload file", type=["csv", "parquet", "tsv"])
        if up:
            try:
                if up.name.endswith(".parquet"):
                    uploaded_df = pd.read_parquet(up)
                else:
                    uploaded_df = pd.read_csv(up)
                table_name = up.name.split(".")[0]
                st.success(f"Loaded {len(uploaded_df):,} rows")
            except Exception as e:
                st.error(f"Read error: {e}")

    zone_up = st.file_uploader(
        "Optional: Taxi Zone Lookup (CSV)",
        type=["csv"],
        help="For JOIN queries, upload a lookup with columns like LocationID and Borough.",
    )
    if zone_up:
        try:
            lookup_df = pd.read_csv(zone_up)
            lookup_table_name = zone_up.name.split(".")[0]
            st.success(f"Loaded lookup: {len(lookup_df):,} rows")
        except Exception as e:
            st.error(f"Lookup read error: {e}")
    
    n_rows = st.slider(
        "Sample size (built-in)",
        10_000,
        200_000,
        50_000,
        10_000,
        help="Row count for the selected built-in sample (Yellow Taxi or NYS Tax).",
    )

    st.divider()
    st.markdown("### Engines")
    selected_engines = st.multiselect(
        "Run with",
        list(ENGINES.keys()),
        default=["DuckDB", "Polars", "SQLAlchemy"],
    )

    st.divider()
    st.markdown("### Query")
    active_query_templates = query_templates_for(data_source)
    query_template = st.selectbox(
        "Template",
        list(active_query_templates.keys()),
        key=f"sidebar_query_tpl_{data_source}",
    )
    runs_per_engine = st.slider("Runs per engine", 1, 5, 3,
                                help="Average over N runs for stable timing")

    st.divider()
    _eng_lines = "".join(
        f"{ENGINES[n]['icon']} <b>{n}</b> — {ENGINES[n]['description']}<br>"
        for n in ENGINES
    )
    st.markdown(
        f"""<div style="font-size:0.72rem;color:#6f6a7a;line-height:1.65;">
<b style="color:#8b8798;">Engines</b><br>{_eng_lines}<br>
<b style="color:#8b8798;">Note</b><br>
PySpark and psycopg2 often need extra runtime setup to benchmark in full.
</div>""",
        unsafe_allow_html=True,
    )

# ── Load Data ───────────────────────────────────────────────────────────────────
if uploaded_df is not None:
    df = uploaded_df
elif data_source == "Yellow Taxi Sample (built-in)":
    df = load_yellow_taxi_sample(n_rows)
elif data_source == "NYS Tax Sample (built-in)":
    df = load_nys_sample(n_rows)
else:
    # Upload selected but no file yet — small demo frame so the app stays usable.
    df = load_yellow_taxi_sample(min(10_000, n_rows))

if data_source == "Upload CSV / Parquet" and uploaded_df is None:
    st.info(
        "Upload a rides file in the sidebar, or switch to **Yellow Taxi** / **NYS Tax** "
        "built‑in data. Until a file loads, queries run against a small Yellow Taxi demo sample."
    )

# ── Header ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="dash-header">
  <div class="dash-title">SQL Engine Benchmark</div>
  <div class="dash-subtitle">PySpark · DuckDB · Dask-SQL · SQLAlchemy · psycopg2 · Polars — NYS Tax Data &amp; Beyond</div>
</div>
""", unsafe_allow_html=True)

# ── Overview metrics ─────────────────────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Dataset Rows</div>
        <div class="metric-value">{len(df):,}<span class="metric-unit">rows</span></div>
    </div>""", unsafe_allow_html=True)
with m2:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Columns</div>
        <div class="metric-value">{len(df.columns)}<span class="metric-unit">cols</span></div>
    </div>""", unsafe_allow_html=True)
with m3:
    mem_mb = df.memory_usage(deep=True).sum() / 1e6
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Memory</div>
        <div class="metric-value">{mem_mb:.1f}<span class="metric-unit">MB</span></div>
    </div>""", unsafe_allow_html=True)
with m4:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Engines Selected</div>
        <div class="metric-value">{len(selected_engines)}<span class="metric-unit">/{len(ENGINES)}</span></div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)

st.markdown(
    '<div class="section-header">Engines at a glance</div>',
    unsafe_allow_html=True,
)
st.caption("One-line summary of each engine supported in this dashboard.")
for chunk in range(0, len(ENGINES), 3):
    row_engines = list(ENGINES.items())[chunk : chunk + 3]
    gcols = st.columns(len(row_engines))
    for gc, (ename, emeta) in zip(gcols, row_engines):
        with gc:
            st.markdown(
                f"""<div class="metric-card" style="margin-bottom:0.6rem;padding:0.9rem 1rem;">
<div style="font-weight:700;font-size:1rem;color:{emeta['color']};">{emeta['icon']} {ename}</div>
<div style="font-size:0.8rem;color:#6f6a7a;margin-top:0.45rem;line-height:1.5">{emeta['description']}</div>
</div>""",
                unsafe_allow_html=True,
            )

st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)

# ── Tabs ─────────────────────────────────────────────────────────────────────────
tab_bench, tab_viz, tab_data, tab_schema, tab_guide = st.tabs([
    "⚡ Benchmark", "📊 Query & Visualize", "🗂 Data Preview", "🔬 Schema & Stats", "📖 Engine Guide"
])

# ══════════════════════════════════════════════════════════════════════════════════
# TAB 1 — BENCHMARK
# ══════════════════════════════════════════════════════════════════════════════════
with tab_bench:
    # SQL editor
    st.markdown('<div class="section-header">SQL Query</div>', unsafe_allow_html=True)
    base_sql = active_query_templates[query_template]
    if query_template == "Custom SQL":
        base_sql = "SELECT * FROM {table} LIMIT 20"

    cols = [f'"{c}"' for c in df.columns]
    col_hint = ", ".join(cols[:5]) + ("..." if len(cols) > 5 else "")
    st.caption(
        f"Available columns: `{col_hint}` — use `{{table}}` for main data"
        " and `{lookup_table}` for optional lookup joins."
    )

    st.markdown("**From sidebar template**")
    st.caption("Uses the template selected in the sidebar. Edit below before running if needed.")
    st.text_area(
        "Template SQL",
        value=base_sql,
        height=110,
        key="bench_template_sql",
        label_visibility="collapsed",
    )
    run_bench_template = st.button(
        "▶  Run Benchmark",
        use_container_width=True,
        key="run_bench_template_btn",
    )

    st.markdown("**Custom query**")
    st.caption("Independent of the sidebar template — use its own **Run Custom Query** button.")
    st.text_area(
        "Custom SQL",
        value=st.session_state.get("bench_custom_sql", "SELECT * FROM {table} LIMIT 20"),
        height=130,
        key="bench_custom_sql",
        label_visibility="collapsed",
        help="Write any SQL using {table} and optional {lookup_table}.",
    )
    run_bench_custom = st.button(
        "▶  Run Custom Query",
        use_container_width=True,
        key="run_bench_custom_btn",
    )

    run_btn = run_bench_template or run_bench_custom
    if run_bench_custom:
        sql_query = st.session_state.get(
            "bench_custom_sql", "SELECT * FROM {table} LIMIT 20"
        )
    elif run_bench_template:
        sql_query = st.session_state.get("bench_template_sql", base_sql)
    else:
        sql_query = ""

    if not selected_engines:
        st.warning("Select at least one engine from the sidebar.")
    elif run_btn:
        st.markdown('<div class="section-header" style="margin-top:1.2rem">Execution Log</div>',
                    unsafe_allow_html=True)

        log_lines   = []
        all_results = {}   # engine → {time, status, df}
        prog = st.progress(0)
        log_ph = st.empty()

        def render_log():
            html = "<div class='log-box'>" + "<br>".join(log_lines[-30:]) + "</div>"
            log_ph.markdown(html, unsafe_allow_html=True)

        for i, eng in enumerate(selected_engines):
            cfg = ENGINES[eng]
            times = []
            last_result, last_status = pd.DataFrame(), "skip"

            log_lines.append(
                f'<span class="log-info">[{datetime.now():%H:%M:%S}] '
                f'Starting {cfg["icon"]} {eng}  (×{runs_per_engine})</span>'
            )
            render_log()

            runner = ENGINE_RUNNERS.get(eng)
            if runner is None:
                last_status = "not_installed"
            else:
                for r in range(runs_per_engine):
                    result_df, elapsed, status = runner(
                        df, sql_query, table_name, lookup_df, lookup_table_name
                    )
                    if status == "ok":
                        times.append(elapsed)
                        last_result = result_df
                        last_status = "ok"
                        log_lines.append(
                            f'<span class="log-ok">  run {r+1}: {elapsed*1000:.1f} ms</span>'
                        )
                    else:
                        last_status = status
                        fix_hint = status_fix_hint(status)
                        log_lines.append(
                            f'<span class="log-warn">  run {r+1}: {status}</span><br>'
                            f'<span class="status-skip">  how to fix: {fix_hint}</span>'
                        )
                        break
                    render_log()

            avg_t = float(np.mean(times)) if times else None
            all_results[eng] = {
                "avg_ms": avg_t * 1000 if avg_t else None,
                "runs":   len(times),
                "status": last_status,
                "df":     last_result,
                "times":  [t * 1000 for t in times],
            }
            prog.progress((i + 1) / len(selected_engines))
            render_log()

        prog.empty()

        # ── Results summary table ─────────────────────────────────────────────
        st.markdown('<div class="section-header" style="margin-top:1.5rem">Results</div>',
                    unsafe_allow_html=True)

        # Timing leaderboard
        ok_engines = [(e, v) for e, v in all_results.items()
                      if v["status"] == "ok" and v["avg_ms"] is not None]
        ok_engines.sort(key=lambda x: x[1]["avg_ms"])

        if ok_engines:
            fastest_ms = ok_engines[0][1]["avg_ms"]

            lc, rc = st.columns([3, 2])
            with lc:
                # Bar chart via plotly
                try:
                    import plotly.graph_objects as go
                    eng_names  = [e for e, _ in ok_engines]
                    eng_times  = [v["avg_ms"] for _, v in ok_engines]
                    eng_colors = [ENGINES[e]["color"] for e in eng_names]

                    fig = go.Figure(go.Bar(
                        x=eng_times,
                        y=eng_names,
                        orientation="h",
                        marker_color=eng_colors,
                        marker_line_width=0,
                        text=[f"{t:.1f} ms" for t in eng_times],
                        textposition="outside",
                        textfont=dict(color="#3d3a45", family="JetBrains Mono"),
                    ))
                    fig.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        margin=dict(l=0, r=80, t=10, b=10),
                        xaxis=dict(
                            showgrid=True, gridcolor="#ebe8e4",
                            color="#8b8798", title="Avg latency (ms)",
                        ),
                        yaxis=dict(color="#3d3a45", autorange="reversed"),
                        height=max(200, len(ok_engines) * 55),
                        font=dict(family="Syne"),
                    )
                    st.plotly_chart(fig, use_container_width=True)
                except ImportError:
                    st.info("Install plotly for bar charts: `pip install plotly`")

            with rc:
                for rank, (eng, v) in enumerate(ok_engines, 1):
                    cfg = ENGINES[eng]
                    speedup = v["avg_ms"] / fastest_ms
                    medal = ["🥇","🥈","🥉"][rank-1] if rank <= 3 else f"#{rank}"
                    st.markdown(f"""
<div class="metric-card" style="margin-bottom:0.6rem;border-color:{cfg['color']}44">
  <div style="display:flex;justify-content:space-between;align-items:center">
    <span style="font-size:1.1rem">{medal} {engine_badge(eng)}</span>
  </div>
  <div class="metric-value" style="color:{cfg['color']};font-size:1.5rem">
    {v['avg_ms']:.1f}<span class="metric-unit">ms</span>
  </div>
  <div class="metric-delta {'delta-good' if speedup==1 else 'delta-bad'}">
    {'fastest' if speedup==1 else f'{speedup:.1f}× slower'}
    · {v['runs']} run{'s' if v['runs']!=1 else ''}
  </div>
</div>""", unsafe_allow_html=True)

        # Status summary for all engines
        st.markdown('<div class="section-header" style="margin-top:1rem">All Engines</div>',
                    unsafe_allow_html=True)
        rows = []
        for eng, v in all_results.items():
            rows.append({
                "Engine": eng,
                "Status": v["status"],
                "How to fix": status_fix_hint(v["status"]),
                "Avg (ms)": f"{v['avg_ms']:.2f}" if v["avg_ms"] else "—",
                "Runs": v["runs"],
                "Result Rows": len(v["df"]) if not v["df"].empty else "—",
            })
        summary_df = pd.DataFrame(rows)
        st.dataframe(summary_df, use_container_width=True, hide_index=True)

        # ── Per-engine result previews ──────────────────────────────────────
        if ok_engines:
            st.markdown('<div class="section-header" style="margin-top:1.2rem">Query Result Previews</div>',
                        unsafe_allow_html=True)
            tabs_res = st.tabs([f"{ENGINES[e]['icon']} {e}" for e, _ in ok_engines])
            for tab_r, (eng, v) in zip(tabs_res, ok_engines):
                with tab_r:
                    st.dataframe(v["df"].head(20), use_container_width=True, hide_index=True)

        # ── Run distribution (box plot) ─────────────────────────────────────
        multi_run = [(e, v) for e, v in all_results.items()
                     if v["status"] == "ok" and len(v["times"]) > 1]
        if multi_run:
            try:
                import plotly.graph_objects as go
                fig2 = go.Figure()
                for eng, v in multi_run:
                    fig2.add_trace(go.Box(
                        y=v["times"],
                        name=eng,
                        marker_color=ENGINES[eng]["color"],
                        line_color=ENGINES[eng]["color"],
                        boxmean=True,
                    ))
                fig2.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    yaxis=dict(title="Latency (ms)", gridcolor="#ebe8e4", color="#8b8798"),
                    xaxis=dict(color="#3d3a45"),
                    margin=dict(l=0, r=0, t=20, b=10),
                    height=280,
                    showlegend=False,
                    font=dict(family="Syne"),
                )
                st.markdown('<div class="section-header" style="margin-top:1rem">Run Distribution</div>',
                            unsafe_allow_html=True)
                st.plotly_chart(fig2, use_container_width=True)
            except ImportError:
                pass

# ══════════════════════════════════════════════════════════════════════════════════
# TAB 2 — QUERY & VISUALIZE (single engine + charts)
# ══════════════════════════════════════════════════════════════════════════════════
with tab_viz:
    st.markdown(
        '<div class="section-header">Engine &amp; query</div>',
        unsafe_allow_html=True,
    )
    st.caption(
        "Choose one engine, run your SQL, then explore the result as a table and chart."
    )

    row1 = st.columns([1, 1])
    with row1[0]:
        viz_engine = st.selectbox(
            "Engine",
            list(ENGINES.keys()),
            index=list(ENGINES.keys()).index("DuckDB"),
            format_func=lambda x: f"{ENGINES[x]['icon']} {x}",
            key="viz_engine_sel",
        )
    with row1[1]:
        viz_template = st.selectbox(
            "Template",
            list(active_query_templates.keys()),
            key=f"viz_query_tpl_{data_source}",
        )

    col_hint_v = ", ".join([f'"{c}"' for c in df.columns[:5]])
    if len(df.columns) > 5:
        col_hint_v += ", …"
    st.caption(
        f"Columns: `{col_hint_v}` — use `{{table}}` for main data"
        " and `{lookup_table}` for optional lookup joins."
    )

    base_viz = active_query_templates[viz_template]
    if viz_template == "Custom SQL":
        base_viz = "SELECT * FROM {table} LIMIT 100"

    st.markdown("**From sidebar template**")
    st.text_area(
        "Template SQL",
        value=base_viz,
        height=115,
        key="viz_template_sql",
        label_visibility="collapsed",
    )
    run_viz_template = st.button(
        "▶  Run query",
        use_container_width=True,
        key="viz_run_template_btn",
    )

    st.markdown("**Custom query**")
    st.caption("Runs independently — uses **Run Custom Query** below.")
    st.text_area(
        "Custom SQL",
        value=st.session_state.get("viz_custom_sql", "SELECT * FROM {table} LIMIT 100"),
        height=125,
        key="viz_custom_sql",
        label_visibility="collapsed",
        help="Write any SQL using {table} and optional {lookup_table}.",
    )
    run_viz_custom = st.button(
        "▶  Run Custom Query",
        use_container_width=True,
        key="viz_run_custom_btn",
    )

    viz_run = run_viz_template or run_viz_custom
    if run_viz_custom:
        viz_sql = st.session_state.get("viz_custom_sql", "SELECT * FROM {table} LIMIT 100")
    elif run_viz_template:
        viz_sql = st.session_state.get("viz_template_sql", base_viz)
    else:
        viz_sql = ""

    if viz_run:
        runner_v = ENGINE_RUNNERS.get(viz_engine)
        if runner_v is None:
            st.error("No runner for this engine.")
        else:
            out_df, elapsed_v, status_v = runner_v(
                df, viz_sql, table_name, lookup_df, lookup_table_name
            )
            st.session_state["viz_payload"] = {
                "engine": viz_engine,
                "df": out_df,
                "ms": elapsed_v * 1000.0,
                "status": status_v,
                "sql": viz_sql,
            }

    payload = st.session_state.get("viz_payload")
    if payload is None:
        st.info(
            'Select an engine and click **Run query** or **Run Custom Query** to load '
            'results and charts.'
        )
    elif payload["status"] != "ok":
        st.error(f"Query did not succeed: `{payload['status']}`")
    else:
        res_df = payload["df"]
        veng = payload["engine"]
        vcfg = ENGINES[veng]
        inferred = infer_viz_defaults(res_df)
        auto_kind, auto_x, auto_y = inferred

        st.markdown('<div class="section-header">Result summary</div>', unsafe_allow_html=True)
        vm1, vm2, vm3 = st.columns(3)
        with vm1:
            st.markdown(
                f"""<div class="metric-card"><div class="metric-label">Engine</div>
                <div class="metric-value" style="font-size:1.3rem;color:{vcfg['color']}">
                {vcfg['icon']} {veng}</div></div>""",
                unsafe_allow_html=True,
            )
        with vm2:
            st.markdown(
                f"""<div class="metric-card"><div class="metric-label">Rows</div>
                <div class="metric-value">{len(res_df):,}</div></div>""",
                unsafe_allow_html=True,
            )
        with vm3:
            st.markdown(
                f"""<div class="metric-card"><div class="metric-label">Time</div>
                <div class="metric-value">{payload['ms']:.1f}<span class="metric-unit">ms</span></div></div>""",
                unsafe_allow_html=True,
            )

        st.markdown('<div class="section-header">Query output</div>', unsafe_allow_html=True)
        st.dataframe(res_df, use_container_width=True, hide_index=True, height=min(400, 120 + min(len(res_df), 12) * 35))

        st.markdown('<div class="section-header">Visualization</div>', unsafe_allow_html=True)

        cols_all = list(res_df.columns)
        num_cols_v = res_df.select_dtypes(include=[np.number]).columns.tolist()

        chart_ui_opts = [
            "Auto",
            "Bar chart",
            "Line chart",
            "Scatter plot",
            "Histogram",
            "Table only",
        ]
        chart_ui = st.selectbox("Chart type", chart_ui_opts, key="viz_chart_ui")

        eff_kind, _, _ = map_ui_chart_to_kind(chart_ui, inferred)

        if chart_ui == "Table only":
            st.caption("Chart hidden — scroll the table above for full output.")
        elif not cols_all:
            st.caption("No columns in result.")
        else:
            if chart_ui == "Auto":
                st.caption(
                    f"Auto: **{eff_kind}**"
                    + (f" — `{auto_x}`" if auto_x else "")
                    + (f" vs `{auto_y}`" if auto_y else "")
                )
            x_col = auto_x
            y_col = auto_y

            if chart_ui != "Auto":
                if eff_kind == "histogram" or chart_ui == "Histogram":
                    pick_h = [c for c in cols_all if c in num_cols_v] or cols_all
                    h_idx = pick_h.index(auto_x) if auto_x in pick_h else 0
                    h_col = st.selectbox("Value column", pick_h, index=h_idx, key="viz_hist_col")
                    x_col, y_col = h_col, None
                    eff_kind = "histogram"
                else:
                    ix = cols_all.index(auto_x) if auto_x in cols_all else 0
                    iy = cols_all.index(auto_y) if auto_y in cols_all else min(1, len(cols_all) - 1)
                    cxa, cxb = st.columns(2)
                    with cxa:
                        x_col = st.selectbox("X axis", cols_all, index=ix, key="viz_x_axis")
                    with cxb:
                        y_opts = [c for c in cols_all if c != x_col] or cols_all
                        iy2 = y_opts.index(auto_y) if auto_y in y_opts else min(len(y_opts) - 1, max(0, iy))
                        y_col = st.selectbox("Y axis", y_opts, index=min(iy2, len(y_opts) - 1), key="viz_y_axis")

                    if chart_ui == "Bar chart":
                        eff_kind = "bar"
                    elif chart_ui == "Line chart":
                        eff_kind = "line"
                    else:
                        eff_kind = "scatter"

            if eff_kind != "table":
                render_query_output_chart(
                    res_df, eff_kind, x_col, y_col, vcfg["color"],
                )

# ══════════════════════════════════════════════════════════════════════════════════
# TAB 3 — DATA PREVIEW
# ══════════════════════════════════════════════════════════════════════════════════
with tab_data:
    st.markdown('<div class="section-header">Dataset Preview</div>', unsafe_allow_html=True)

    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        filter_county = st.selectbox(
            "Filter by County",
            ["All"] + (sorted(df["County"].unique().tolist())
                       if "County" in df.columns else []),
        )
    with fc2:
        n_preview = st.slider("Rows to show", 10, 500, 50, 10)
    with fc3:
        sort_col = st.selectbox("Sort by", ["(none)"] + df.columns.tolist())

    preview = df.copy()
    if filter_county != "All" and "County" in preview.columns:
        preview = preview[preview["County"] == filter_county]
    if sort_col != "(none)":
        preview = preview.sort_values(sort_col, ascending=False)

    st.dataframe(preview.head(n_preview), use_container_width=True, height=400)
    st.caption(f"Showing {min(n_preview, len(preview)):,} of {len(preview):,} rows")

    # Quick numeric distribution
    st.markdown('<div class="section-header" style="margin-top:1rem">Numeric Column Distribution</div>',
                unsafe_allow_html=True)
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    if num_cols:
        dist_col = st.selectbox("Column", num_cols)
        try:
            import plotly.express as px
            fig_h = px.histogram(
                df, x=dist_col, nbins=50,
                color_discrete_sequence=[ENGINES["DuckDB"]["color"]],
            )
            fig_h.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                yaxis=dict(gridcolor="#ebe8e4", color="#8b8798"),
                xaxis=dict(color="#8b8798"),
                margin=dict(l=0, r=0, t=10, b=10),
                height=260, showlegend=False,
                font=dict(family="Syne"),
            )
            st.plotly_chart(fig_h, use_container_width=True)
        except ImportError:
            st.bar_chart(df[dist_col].value_counts().head(30))

# ══════════════════════════════════════════════════════════════════════════════════
# TAB 4 — SCHEMA & STATS
# ══════════════════════════════════════════════════════════════════════════════════
with tab_schema:
    st.markdown('<div class="section-header">Schema</div>', unsafe_allow_html=True)
    schema_rows = []
    for col in df.columns:
        null_pct = df[col].isna().mean() * 100
        uniq     = df[col].nunique()
        schema_rows.append({
            "Column":    col,
            "dtype":     str(df[col].dtype),
            "Non-Null %": f"{100-null_pct:.1f}%",
            "Unique":    f"{uniq:,}",
            "Sample":    str(df[col].dropna().iloc[0]) if not df[col].dropna().empty else "—",
        })
    st.dataframe(pd.DataFrame(schema_rows), use_container_width=True, hide_index=True)

    st.markdown('<div class="section-header" style="margin-top:1rem">Descriptive Statistics</div>',
                unsafe_allow_html=True)
    st.dataframe(df.describe().T, use_container_width=True)

    # Correlation
    num_df = df.select_dtypes(include=np.number)
    if len(num_df.columns) >= 2:
        st.markdown('<div class="section-header" style="margin-top:1rem">Correlation Matrix</div>',
                    unsafe_allow_html=True)
        try:
            import plotly.express as px
            corr = num_df.corr().round(2)
            fig_c = px.imshow(
                corr, text_auto=True, aspect="auto",
                color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
            )
            fig_c.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=0, t=10, b=10),
                font=dict(family="Syne", color="#3d3a45"),
                height=380,
            )
            st.plotly_chart(fig_c, use_container_width=True)
        except ImportError:
            st.dataframe(num_df.corr().round(3), use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════════
# TAB 5 — ENGINE GUIDE
# ══════════════════════════════════════════════════════════════════════════════════
with tab_guide:
    st.markdown('<div class="section-header">Engine Reference</div>', unsafe_allow_html=True)

    guide_data = [
        ("DuckDB",     "🦆", "pip install duckdb",
         "In-process OLAP engine. Blazing fast for analytical queries on DataFrames, CSVs, Parquet. Zero config.",
         "✅ Fastest for local analytics", "❌ Single-node only"),
        ("Polars",     "🐻‍❄️", "pip install polars",
         "Rust-powered DataFrame library with built-in SQL context. Excellent memory efficiency and parallelism.",
         "✅ Memory-efficient, Rust speed", "❌ SQL dialect differences"),
        ("SQLAlchemy", "🔗", "pip install sqlalchemy",
         "Python SQL toolkit and ORM. Works with any DB (SQLite, Postgres, MySQL, etc.) via dialect plugins.",
         "✅ Universal DB adapter", "❌ ORM overhead for bulk ops"),
        ("psycopg2",   "🐘", "pip install psycopg2-binary",
         "Native PostgreSQL adapter. Requires a running Postgres instance. Best for production PG workloads.",
         "✅ Native PG performance", "❌ Needs external Postgres"),
        ("PySpark",    "🔥", "pip install pyspark",
         "Apache Spark Python API. Distributed, handles terabyte-scale data across clusters. JVM startup overhead.",
         "✅ Scales to TB+, cluster-ready", "❌ JVM overhead, slow locally"),
        ("Dask-SQL",   "⚙️", "pip install dask-sql",
         "SQL layer on Dask DataFrames. Parallelises pandas operations across cores; cluster-friendly.",
         "✅ Familiar SQL on large CSVs", "❌ Less mature than Spark"),
    ]

    for name, icon, install, desc, pro, con in guide_data:
        cfg = ENGINES[name]
        with st.expander(f"{icon} {name}", expanded=False):
            gc1, gc2 = st.columns([2, 1])
            with gc1:
                st.markdown(f"**{desc}**")
                st.markdown(f"<span class='delta-good'>{pro}</span><br>"
                            f"<span class='delta-bad'>{con}</span>",
                            unsafe_allow_html=True)
            with gc2:
                st.markdown(f"""<div class="query-box">{install}</div>""",
                            unsafe_allow_html=True)

    st.divider()
    st.markdown('<div class="section-header">Choosing the Right Engine</div>',
                unsafe_allow_html=True)

    advice = {
        "Small–Medium data (<1 GB), single machine": "🦆 DuckDB or 🐻‍❄️ Polars",
        "Production app backed by PostgreSQL": "🐘 psycopg2 + 🔗 SQLAlchemy",
        "Multi-core laptop, data > RAM": "⚙️ Dask-SQL",
        "Cluster / Hadoop / cloud data lake (TB+)": "🔥 PySpark",
        "Exploratory analysis in notebook": "🦆 DuckDB or 🐻‍❄️ Polars",
        "ORM + migrations + schema management": "🔗 SQLAlchemy",
    }
    for scenario, recommendation in advice.items():
        st.markdown(
            f"**{scenario}** → {recommendation}"
        )

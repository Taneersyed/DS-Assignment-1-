# NYC Congestion Pricing Audit - How to Run

This project implements a Big Data pipeline to analyze 147M+ taxi trips using DuckDB and Parquet on a local machine.

## Prerequisites

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *Note: If `duckdb` installation fails, try `pip install duckdb --upgrade` to get the latest pre-compiled wheel.*

## Steps to Run

### 1. Run the Pipeline
Execute the main ETL script. This will download data (if missing), impute December 2025 data, and perform all analyses using DuckDB.
```bash
python pipeline.py
```
*Expected Output:*
- Downloads parquet files to `data_downloads/`.
- Imputes missing Dec 2025 data.
- Generates `output/ghost_trip_audit.csv`, `output/impact_stats.json`, etc.

### 2. Generate PDF Report
Create the Executive Summary PDF.
```bash
python generate_report.py
```
*Output:* `audit_report.pdf`

### 3. Launch Dashboard
Visualize the results in the interactive Streamlit dashboard.
```bash
streamlit run dashboard.py
```

## Project Structure

- `pipeline.py`: Main ETL script (DuckDB + Parquet).
- `dashboard.py`: Streamlit dashboard code.
- `generate_report.py`: Script to generate PDF report.
- `BLOG_POSTS.md`: Drafts for LinkedIn and Medium posts.
- `data_downloads/`: Raw Parquet files (partitioned by year/type).
- `output/`: Aggregated CSVs and JSON stats for the dashboard.

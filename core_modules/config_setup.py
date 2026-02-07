"""
Market Analysis Toolkit - Configuration & Setup
===============================================

This module contains configuration details and execution instructions for the Market Analysis Toolkit.
"""

# ============================================================================
# PROJECT STRUCTURE
# ============================================================================

PROJECT_STRUCTURE = """
📁 Market Analysis Toolkit
 
├── 📄 run_analysis.py             # Main entry point (Orchestrator)
├── 📁 core_modules/               # Core logic modules
│   ├── 📄 data_ingestion.py       # Data acquisition (formerly WebScraping)
│   ├── 📄 processing_engine.py    # Main ETL & Analytics engine
│   ├── 📄 report_builder.py       # PDF summary generator
│   ├── 📄 content_generator.py    # Content asset generator
│   ├── 📄 analytics_dashboard.py  # Interactive Dashboard
│   ├── 📄 config_setup.py         # This file
│   └── 📄 system_check.py         # Integrity verification script
│
├── 📁 data_downloads/             # Raw transaction data (Parquet)
│
├── 📁 output/                     # Analysis artifacts
│   ├── market_stats.json          # Key metrics
│   ├── anomaly_audit.csv          # Flagged irregular transactions
│   ├── leakage_report.csv         # Revenue leakage analysis
│   ├── market_summary.pdf         # Executive PDF report
│   ├── white_paper.md             # Technical retrospective
│   ├── summary_post.md            # Professional brief
│   ├── micro_thread.md            # Social media assets
│   ├── presentation_slides.json   # JSON data for slide decks
│   └── CONTENT_README.md          # Content guide
│
└── 📁 cache/                      # Temporary storage
    └── external_factors_2025.csv  # Cached external data
"""

# ============================================================================
# QUICK START
# ============================================================================

QUICK_START = """
QUICK START - Execute Market Analysis
=====================================

STEP 1: Install Dependencies
----------------------------
pip install polars duckdb pyarrow pandas requests scipy reportlab streamlit plotly

STEP 2: Run the Full Toolkit
----------------------------
python run_analysis.py

# This orchestrator will:
# 1. Acquire necessary transaction data
# 2. Run the processing engine (ETL + Analytics)
# 3. Generate the PDF executive summary
# 4. Create content assets (White paper, posts)
# 5. Launch the interactive dashboard

STEP 3: Verify Integrity
------------------------
python core_modules/system_check.py

# Checks all modules and output artifacts.
"""

# ============================================================================
# CONFIGURATION DETAILS
# ============================================================================

CONFIGURATION = """
CONFIGURATION
=============

Data Sources
------------
Data acquisition is handled by 'core_modules/data_ingestion.py'.
Target: Public NYC TLC Data (Yellow/Green Taxi).

Analysis Parameters (in processing_engine.py)
---------------------------------------------
- Target Region: Core Economic Zone (Manhattan south of 60th)
- Comparison Period: Q1 2024 vs Q1 2025
- Anomaly Thresholds:
  * Momentum Index > 65.0
  * Time Delta < 1.0 min
  * Value Mismatch > $20.00

Dashboard Settings
------------------
- Port: Default Streamlit port (8501)
- Layout: Wide mode by default

"""

# ============================================================================
# EXPORT GUIDE
# ============================================================================

if __name__ == "__main__":
    readme_path = "README_SETUP.txt"
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("MARKET ANALYSIS TOOLKIT - SETUP GUIDE\n")
        f.write("=" * 60 + "\n\n")
        f.write(PROJECT_STRUCTURE + "\n\n")
        f.write(QUICK_START + "\n\n")
        f.write(CONFIGURATION + "\n\n")
        
    print(f"✅ Setup guide generated: {readme_path}")

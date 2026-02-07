#!/usr/bin/env python
"""
Verification Script - Check Market Analysis Toolkit Integrity
"""

import os
import sys
from pathlib import Path

def check_file(path, description):
    """Check if a file exists and report."""
    if os.path.exists(path):
        size = os.path.getsize(path)
        if size < 1024:
            size_str = f"{size} B"
        elif size < 1024*1024:
            size_str = f"{size/1024:.1f} KB"
        else:
            size_str = f"{size/(1024*1024):.1f} MB"
        print(f"  ✅ {description:.<50} {size_str:>10}")
        return True
    else:
        print(f"  ❌ {description:.<50} MISSING")
        return False

def check_directory(path, description):
    """Check if a directory exists."""
    if os.path.isdir(path):
        count = len(os.listdir(path))
        print(f"  ✅ {description:.<50} {count:>10} items")
        return True
    else:
        print(f"  ❌ {description:.<50} MISSING")
        return False

def main():
    """Run all verification checks."""
    
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║        MARKET ANALYSIS TOOLKIT - SYSTEM INTEGRITY CHECK        ║
    ║                                                                ║
    ║  Verifying core modules and data assets...                     ║
    ╚════════════════════════════════════════════════════════════════╝
    """)
    
    # Track success
    all_ok = True
    
    # Check Python scripts
    print("\n📝 Core Modules")
    print("-" * 65)
    scripts = {
        'core_modules/processing_engine.py': 'Analysis Engine',
        'core_modules/analytics_dashboard.py': 'Interactive Dashboard',
        'core_modules/report_builder.py': 'Report Generator',
        'core_modules/content_generator.py': 'Content Creator',
        'core_modules/data_ingestion.py': 'Data Ingestion',
        'run_analysis.py': 'Main Orchestrator',
        'core_modules/config_setup.py': 'Configuration',
    }
    
    for script, desc in scripts.items():
        all_ok &= check_file(script, desc)
    
    # Check data files
    print("\n📊 Data Assets")
    print("-" * 65)
    data_files = {
        'data_downloads/2023_green_unified.csv': '2023 Grn Data',
        'data_downloads/2023_yellow_unified.csv': '2023 Ylw Data',
        'data_downloads/2024_green_unified.csv': '2024 Grn Data',
        'data_downloads/2024_yellow_unified.csv': '2024 Ylw Data',
        'data_downloads/2025_green_unified.csv': '2025 Grn Data',
        'data_downloads/2025_yellow_unified.csv': '2025 Ylw Data',
    }
    
    for data_file, desc in data_files.items():
        all_ok &= check_file(data_file, desc)
    
    # Check directories
    print("\n📁 System Directories")
    print("-" * 65)
    dirs = {
        'data_downloads': 'Raw Data Store',
        'output': 'Analysis Output',
        'cache': 'System Cache',
    }
    
    for dir_path, desc in dirs.items():
        check_directory(dir_path, desc)
    
    # Check documentation
    print("\n📖 Documentation")
    print("-" * 65)
    docs = {
        'output/white_paper.md': 'Technical White Paper',
        'output/market_summary.pdf': 'Executive Report',
    }
    
    for doc, desc in docs.items():
        # These might not exist yet if pipeline hasn't run
        if os.path.exists(doc):
             check_file(doc, desc)
        else:
             print(f"  ⚠️ {desc:.<50} (Not Generated Yet)")
    
    # Summary
    print("\n" + "=" * 65)
    
    if all_ok:
        print("✅ SYSTEM CHECK PASSED")
        print("\nAll core components are active.")
        print("\nNext Steps:")
        print("  1. python run_analysis.py          (Execute Analysis)")
        print("  2. streamlit run core_modules/analytics_dashboard.py (Launch Dashboard)")
    else:
        print("❌ SYSTEM CHECK FAILED")
        print("\nCritical components missing. Check installation.")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

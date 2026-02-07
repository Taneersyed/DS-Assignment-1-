import subprocess
import sys
import time
import os

def main():
    print("=========================================")
    print("      Market Trend Analysis Tool         ")
    print("=========================================")

    # 1. Run Data Ingestion
    print(f"\n[1/5] Ingesting Market Data Streams...")
    try:
        subprocess.run([sys.executable, os.path.join("core_modules", "data_ingestion.py")], check=True)
    except subprocess.CalledProcessError:
        print("Error encountered in data_ingestion.py. Stopping.")
        return

    # 2. Run Pipeline
    print(f"\n[2/5] Running Processing Engine...")
    try:
        subprocess.run([sys.executable, os.path.join("core_modules", "processing_engine.py")], check=True)
    except subprocess.CalledProcessError:
        print("Error encountered in processing_engine.py. Stopping.")
        return

    # 3. Generate Report
    print(f"\n[3/5] Generating Executive Summary...")
    try:
        subprocess.run([sys.executable, os.path.join("core_modules", "report_builder.py")], check=True)
    except subprocess.CalledProcessError:
        print("Error encountered in report_builder.py. Stopping.")
        return

    # 4. Generate Blogs
    print(f"\n[4/5] Generating Content Assets...")
    try:
        subprocess.run([sys.executable, os.path.join("core_modules", "content_generator.py")], check=True)
    except subprocess.CalledProcessError:
        print("Error encountered in content_generator.py. Stopping.")
        return

    # 5. Launch Dashboard
    print(f"\n[5/5] Launching Analytics Dashboard...")
    print("Press Ctrl+C to stop the dashboard server.")
    dashboard_path = os.path.join("core_modules", "analytics_dashboard.py")
    try:
        # Use python -m streamlit to ensure we use the correct environment
        subprocess.run([sys.executable, "-m", "streamlit", "run", dashboard_path], check=True)
    except KeyboardInterrupt:
        print("\nDashboard stopped by user.")
    except Exception as e:
        print(f"Error launching dashboard: {e}")

if __name__ == "__main__":
    main()

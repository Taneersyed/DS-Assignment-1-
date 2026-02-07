"""
Generate Executive Summary
==========================
Generates a PDF Executive Summary from the Market Analysis data.
"""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import json
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
PDF_FILE = os.path.join(OUTPUT_DIR, "market_summary.pdf")

def generate_pdf():
    print(f"Generating {PDF_FILE}...")
    
    # Load Data
    stats = {}
    if os.path.exists(f"{OUTPUT_DIR}/market_stats.json"):
        with open(f"{OUTPUT_DIR}/market_stats.json", 'r') as f:
            stats = json.load(f)
            
    anomaly_count = stats.get('anomaly_count', 0)
        
    correlation_text = "N/A"
    if os.path.exists(f"{OUTPUT_DIR}/correlation_summary.txt"):
        with open(f"{OUTPUT_DIR}/correlation_summary.txt", 'r') as f:
            correlation_text = f.read()

    # Create PDF
    c = canvas.Canvas(PDF_FILE, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 50, "Market Trend Analysis Report")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, "Date: January 2026")
    c.drawString(50, height - 100, "Prepared by: Analytics Team")
    
    # Overview
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 140, "1. Executive Overview")
    
    c.setFont("Helvetica", 12)
    y = height - 170
    
    rev = stats.get('revenue_2025', 0)
    c.drawString(70, y, f"Total Projected Revenue: ${rev:,.2f}")
    y -= 25
    
    c.drawString(70, y, f"Total Data Anomalies Flagged: {anomaly_count}")
    y -= 25
    
    vol_change = stats.get('q1_pct_change', 0)
    c.drawString(70, y, f"Q1 Transaction Volume Delta: {vol_change:.2f}%")
    y -= 40
    
    # Top Vendors
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "2. Top 5 Anomalous Sources")
    y -= 30
    c.setFont("Helvetica", 12)
    
    vendors = stats.get('suspicious_vendors', [])
    if vendors:
        for v_id, count in vendors:
            c.drawString(70, y, f"Source ID {v_id}: {count} flagged records")
            y -= 25
    else:
        c.drawString(70, y, "No anomaly sources detected.")
        y -= 25
        
    y -= 15

    # Recommendations
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "3. Strategic Recommendations")
    y -= 30
    
    c.setFont("Helvetica", 12)
    recommendations = [
        "- Adjust dynamic pricing during high volatility periods.",
        "- Audit Top 5 Sources (listed above) for data consistency.",
        "- Increase monitoring at regional boundaries to reduce leakage.",
        "- Implement retention strategies to offset engagement decline."
    ]
    
    for rec in recommendations:
        c.drawString(70, y, rec)
        y -= 20
        
    # Correlation
    y -= 20
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "4. External Factor Correlation")
    y -= 30
    c.setFont("Helvetica", 12)
    
    lines = correlation_text.split('\n')
    for line in lines:
        if line.strip():
            c.drawString(70, y, line)
            y -= 20
            
    c.save()
    print(f"PDF Report saved to {PDF_FILE}")

if __name__ == "__main__":
    generate_pdf()

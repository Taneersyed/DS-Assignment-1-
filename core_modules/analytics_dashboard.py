"""
Market Analytics Dashboard
==========================
Interactive dashboard visualizing market trend analysis results.
Tabs:
1. Regional Volatility (Border Effect)
2. Momentum Analysis (Velocity)
3. Engagement Metrics (Economics)
4. External Factors (Weather)
"""

import os
import json
import warnings
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Market Trend Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
CACHE_DIR = os.path.join(BASE_DIR, "cache")

# ============================================================================
# DATA LOADING
# ============================================================================

@st.cache_data
def load_data():
    """Load all analysis outputs."""
    data = {}
    
    # 1. Stats
    if os.path.exists(f"{OUTPUT_DIR}/market_stats.json"):
        with open(f"{OUTPUT_DIR}/market_stats.json", 'r') as f:
            data['stats'] = json.load(f)
            
    # 2. CSVs
    files = {
        'anomalies': f"{OUTPUT_DIR}/anomaly_audit.csv",
        'leakage': f"{OUTPUT_DIR}/leakage_report.csv",
        'volatility': f"{OUTPUT_DIR}/regional_volatility.csv",
        'momentum_2024': f"{OUTPUT_DIR}/momentum_2024.csv",
        'momentum_2025': f"{OUTPUT_DIR}/momentum_2025.csv",
        'transactions': f"{OUTPUT_DIR}/daily_transactions_2025.csv",
        'engagement': f"{OUTPUT_DIR}/engagement_metrics.csv",
        'factors': f"{CACHE_DIR}/external_factors_2025.csv"
    }
    
    for key, path in files.items():
        if os.path.exists(path):
            try:
                data[key] = pd.read_csv(path)
            except Exception as e:
                st.error(f"Error loading {key}: {e}")
    
    # 3. Text
    if os.path.exists(f"{OUTPUT_DIR}/correlation_summary.txt"):
        with open(f"{OUTPUT_DIR}/correlation_summary.txt", 'r') as f:
            data['correlation_text'] = f.read()
            
    return data

DATA = load_data()

# ============================================================================
# TAB 1: REGIONAL VOLATILITY
# ============================================================================

def tab_volatility():
    st.header("🗺️ Tab 1: Regional Volatility")
    st.markdown("""
        **Analysis**: Identifying regions with anomalous transaction volume shifts.
        Comparing Drop-off volumes in Q1 2024 vs Q1 2025.
    """)
    
    df = DATA.get('volatility')
    if df is not None and not df.empty:
        # Filter for significant volume
        df = df[df['count_2024'] > 100]
        
        # Sort by pct change
        df = df.sort_values('pct_change', ascending=False)
        
        # Top 15 Increases
        top_inc = df.head(15)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            fig = px.bar(
                top_inc,
                x='pct_change',
                y='location_id',
                orientation='h',
                title='Top 15 Regions with Volume Increases',
                labels={'pct_change': '% Change', 'location_id': 'Region ID'},
                color='pct_change',
                color_continuous_scale='Reds'
            )
            fig.update_layout(yaxis={'type': 'category'})
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.write("#### Detailed Metrics")
            st.dataframe(
                top_inc[['location_id', 'count_2024', 'count_2025', 'pct_change']]
                .style.format({'pct_change': '{:.1f}%'})
            )
            
        st.info("High volatility regions suggest displacement effects from the new fee structure.")
    else:
        st.warning("No volatility data available. Run the analysis engine first.")

# ============================================================================
# TAB 2: MOMENTUM ANALYSIS
# ============================================================================

def tab_momentum():
    st.header("⚡ Tab 2: Market Momentum (Velocity)")
    st.markdown("**Hypothesis**: Did the fee structure increase transaction velocity in the core zone?")
    
    v24 = DATA.get('momentum_2024')
    v25 = DATA.get('momentum_2025')
    
    if v24 is not None and v25 is not None:
        col1, col2 = st.columns(2)
        
        def make_heatmap(df, year):
            # df columns: dow, hour, avg_momentum
            pivot = df.pivot_table(index='dow', columns='hour', values='avg_momentum')
            
            days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
            
            # Reindex if possible
            existing_indices = pivot.index
            mapped_indices = [days[i] for i in existing_indices if i < 7]
            
            fig = px.imshow(
                pivot,
                labels=dict(x="Hour of Day", y="Day of Week", color="Momentum Index"),
                y=mapped_indices if len(mapped_indices) == len(existing_indices) else pivot.index,
                title=f"Q1 {year} Momentum Profile",
                color_continuous_scale='Viridis',
                aspect="auto"
            )
            return fig

        with col1:
            st.plotly_chart(make_heatmap(v24, 2024), use_container_width=True)
        with col2:
            st.plotly_chart(make_heatmap(v25, 2025), use_container_width=True)
            
        # Comparison delta
        avg24 = v24['avg_momentum'].mean()
        avg25 = v25['avg_momentum'].mean()
        delta = avg25 - avg24
        pct = (delta / avg24) * 100 if avg24 != 0 else 0
        
        st.metric("Overall Momentum Shift", f"{delta:.2f} Index Points", f"{pct:.1f}%")
        
    else:
        st.warning("Momentum data missing.")

# ============================================================================
# TAB 3: ENGAGEMENT METRICS
# ============================================================================

def tab_engagement():
    st.header("💰 Tab 3: Engagement Economics")
    st.markdown("**Hypothesis**: Does the primary fee crowd out secondary value exchange?")
    
    eng = DATA.get('engagement')
    
    if eng is not None:
        # eng: month, avg_fee, avg_engagement_score
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Bar(name="Avg Fee ($)", x=eng['month'], y=eng['avg_fee'], marker_color='red', opacity=0.5),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(name="Engagement Score", x=eng['month'], y=eng['avg_engagement_score'], mode='lines+markers', line=dict(color='blue')),
            secondary_y=True
        )
        
        fig.update_layout(title="Monthly Fee vs Engagement Score (2025)")
        fig.update_xaxes(title_text="Month")
        fig.update_yaxes(title_text="Fee ($)", secondary_y=False)
        fig.update_yaxes(title_text="Engagement Index", secondary_y=True)
        
        st.plotly_chart(fig, use_container_width=True)
        
        correlation = eng['avg_fee'].corr(eng['avg_engagement_score'])
        st.write(f"**Correlation Coefficient**: {correlation:.3f}")
        if correlation < -0.3:
            st.error("Negative correlation detected: Higher fees align with lower engagement.")
        else:
            st.success("No strong negative correlation detected.")
            
    else:
        st.warning("Engagement data missing.")

# ============================================================================
# TAB 4: EXTERNAL FACTORS
# ============================================================================

def tab_factors():
    st.header("🌧️ Tab 4: External Factors")
    st.markdown("**Hypothesis**: Elasticity of demand relative to external conditions.")
    
    trans = DATA.get('transactions')
    factors = DATA.get('factors')
    
    if trans is not None and factors is not None:
        # Merge
        try:
            trans['date'] = pd.to_datetime(trans['date'])
            factors['date'] = pd.to_datetime(factors['date'])
            merged = pd.merge(trans, factors, on='date')
        except:
             st.error("Date format mismatch between transaction and factor data")
             return

        col1, col2 = st.columns([2, 1])
        with col1:
            fig = px.scatter(
                merged, 
                x='factor_value', 
                y='transactions', 
                trendline='ols',
                title="Daily Transactions vs External Factor (2025)",
                labels={'factor_value': 'Factor Intensity', 'transactions': 'Transaction Volume'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.write("### Analysis")
            if 'correlation_text' in DATA:
                st.text(DATA['correlation_text'])
            
            corr = merged['transactions'].corr(merged['factor_value'])
            st.metric("Correlation", f"{corr:.3f}")
            
            if abs(corr) < 0.3:
                st.info("Demand is Inelastic (External factors have low impact).")
            else:
                st.info("Demand is Elastic (External factors drive volume).")

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    st.sidebar.title("Navigation")
    tab = st.sidebar.radio("Go to", ["Overview", "Volatility", "Momentum", "Engagement", "External Factors"])
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Key Metrics")
    
    stats = DATA.get('stats', {})
    if stats:
        st.sidebar.metric("YTD Revenue", f"${stats.get('revenue_2025', 0):,.0f}")
        val = stats.get('q1_pct_change', 0)
        st.sidebar.metric("Q1 Vol Delta", f"{val:.2f}%")
        
    audit = DATA.get('anomalies')
    if audit is not None:
        st.sidebar.metric("Anomalies Flagged", f"{len(audit):,}")

    if tab == "Overview":
        st.title("📈 Market Trend Analysis Dashboard")
        st.markdown("### Executive Summary")
        st.write("This dashboard visualizes the 2025 market structure changes and their impact on efficiency.")
        
        leakage = DATA.get('leakage')
        if leakage is not None:
            st.markdown("### 🚨 Revenue Leakage Alert")
            st.write("Top regions with compliant transaction failures:")
            st.dataframe(leakage.head(5))
            
        if stats:
            st.info(f"Total Projected Revenue 2025: **${stats.get('revenue_2025', 0):,.2f}**")
            
    elif tab == "Volatility":
        tab_volatility()
    elif tab == "Momentum":
        tab_momentum()
    elif tab == "Engagement":
        tab_engagement()
    elif tab == "External Factors":
        tab_factors()

if __name__ == "__main__":
    main()

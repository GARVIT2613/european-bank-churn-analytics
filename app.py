# Master Streamlit dashboard orchestrating the 5 analytical tabs
import streamlit as st
import pandas as pd
from src.data_loader import load_raw_banking_data
from src.segmentation_engine import apply_customer_segmentation
from src.kpi_metrics import compute_executive_banking_kpis
from src.simulation import run_retention_simulation
from src.visuals import (
    build_capital_flow_bar,
    build_portfolio_sunburst,
    build_tenure_churn_curve,
    build_credit_score_box,
    build_cross_border_churn_bar,
    build_regional_capital_loss_donut,
    build_geo_activity_matrix,
    build_balance_salary_geo_scatter,
    build_age_risk_dual_axis,
    build_product_saturation_bar,
    build_gender_disparity_waterfall,
    build_engagement_heatmap,
    build_high_value_quadrant_matrix,
    build_zero_vs_funded_donut,
    build_top_decile_loss_bar,
    build_tenure_high_value_bar,
    build_retention_waterfall,
    build_retention_sensitivity_heatmap,
    build_product_migration_model,
    build_regulatory_gauge
)

# Page Setup
st.set_page_config(
    page_title="European Banking: Customer Segmentation & Churn Intelligence",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS Styling
try:
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# Data Ingestion & Transformation
raw_df = load_raw_banking_data("data/raw/European_Bank.csv")
df_master = apply_customer_segmentation(raw_df)

# ---------------------------------------------------------
# Sidebar Filter Controls
# ---------------------------------------------------------
st.sidebar.markdown("### 🏦 Portfolio Filters")

selected_countries = st.sidebar.multiselect(
    "Country / Geography",
    options=df_master['Geography'].unique().tolist(),
    default=df_master['Geography'].unique().tolist()
)

selected_genders = st.sidebar.multiselect(
    "Customer Gender",
    options=df_master['Gender'].unique().tolist(),
    default=df_master['Gender'].unique().tolist()
)

age_slider = st.sidebar.slider(
    "Customer Age Range",
    min_value=int(df_master['Age'].min()),
    max_value=int(df_master['Age'].max()),
    value=(18, 85)
)

selected_credit_tiers = st.sidebar.multiselect(
    "Credit Score Tier",
    options=df_master['Credit_Tier'].dropna().unique().tolist(),
    default=df_master['Credit_Tier'].dropna().unique().tolist()
)

active_toggle = st.sidebar.selectbox(
    "Activity Status Filter",
    options=["All Accounts", "Active Members Only", "Inactive Members Only"]
)

# Apply Cross-Filters
filtered_df = df_master[
    (df_master['Geography'].isin(selected_countries)) &
    (df_master['Gender'].isin(selected_genders)) &
    (df_master['Age'] >= age_slider[0]) &
    (df_master['Age'] <= age_slider[1]) &
    (df_master['Credit_Tier'].isin(selected_credit_tiers))
]

if active_toggle == "Active Members Only":
    filtered_df = filtered_df[filtered_df['IsActiveMember'] == 1]
elif active_toggle == "Inactive Members Only":
    filtered_df = filtered_df[filtered_df['IsActiveMember'] == 0]

# Calculate Portfolio KPIs
kpis = compute_executive_banking_kpis(filtered_df)

# ---------------------------------------------------------
# Main Header & Top Executive Metric Cards
# ---------------------------------------------------------
st.title("🏦 European Banking: Customer Segmentation & Churn Analytics")
st.caption("European Central Bank Regulatory Framework • Portfolio Capital at Risk & Retention Diagnostics")

col1, col2, col3, col4 = st.columns(4)
col1.markdown(f"""<div class="kpi-card">
    <div class="kpi-title">Active Account Portfolio</div>
    <div class="kpi-value">{kpis['total_customers']:,} Accounts</div>
    <span class="badge-neu">€{kpis['total_capital']/1e6:.2f}M Total Balance</span>
</div>""", unsafe_allow_html=True)

col2.markdown(f"""<div class="kpi-card">
    <div class="kpi-title">Blended Churn Rate</div>
    <div class="kpi-value">{kpis['churn_rate']:.2f}%</div>
    <span class="{'badge-neg' if kpis['churn_rate'] > 20.0 else 'badge-pos'}">{kpis['churned_customers']:,} Exited Accounts</span>
</div>""", unsafe_allow_html=True)

col3.markdown(f"""<div class="kpi-card">
    <div class="kpi-title">Capital at Risk (Lost Balance)</div>
    <div class="kpi-value">€{kpis['churned_balance']/1e6:.2f}M</div>
    <span class="badge-neg">{kpis['capital_at_risk_pct']:.1f}% Portfolio Exposure</span>
</div>""", unsafe_allow_html=True)

col4.markdown(f"""<div class="kpi-card">
    <div class="kpi-title">High-Value Flight Risk</div>
    <div class="kpi-value">{kpis['hv_churn_rate']:.1f}%</div>
    <span class="badge-neg">Top 25% Balance Tier</span>
</div>""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 5 Tab Visual Dashboard Canvas (2x2 Grid per Tab)
# ---------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Executive Portfolio Overview",
    "🌍 Geographic & Cross-Border Exposure",
    "👥 Demographic & Journey Diagnostics",
    "💎 High-Value Capital Risk Explorer",
    "⚡ What-If Retention Engine"
])

# TAB 1: EXECUTIVE PORTFOLIO OVERVIEW
with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Capital Flow: Retained vs. Lost Balance")
        st.plotly_chart(build_capital_flow_bar(filtered_df), use_container_width=True)
    with c2:
        st.subheader("Multi-Level Portfolio Hierarchy")
        st.plotly_chart(build_portfolio_sunburst(filtered_df), use_container_width=True)
        
    c3, c4 = st.columns(2)
    with c3:
        st.subheader("Customer Tenure vs. Churn Probability")
        st.plotly_chart(build_tenure_churn_curve(filtered_df), use_container_width=True)
    with c4:
        st.subheader("Credit Score Distribution by Churn Status")
        st.plotly_chart(build_credit_score_box(filtered_df), use_container_width=True)

# TAB 2: GEOGRAPHIC & CROSS-BORDER EXPOSURE
with tab2:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Cross-Border Churn Benchmark")
        st.plotly_chart(build_cross_border_churn_bar(filtered_df), use_container_width=True)
    with c2:
        st.subheader("Regional Capital Loss Share")
        st.plotly_chart(build_regional_capital_loss_donut(filtered_df), use_container_width=True)
        
    c3, c4 = st.columns(2)
    with c3:
        st.subheader("Geo-Activity Interaction Matrix")
        st.plotly_chart(build_geo_activity_matrix(filtered_df), use_container_width=True)
    with c4:
        st.subheader("Balance vs. Estimated Salary by Country")
        st.plotly_chart(build_balance_salary_geo_scatter(filtered_df), use_container_width=True)

# TAB 3: DEMOGRAPHIC & JOURNEY DIAGNOSTICS
with tab3:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Age Bracket Churn Risk Curve")
        st.plotly_chart(build_age_risk_dual_axis(filtered_df), use_container_width=True)
    with c2:
        st.subheader("Product Multi-Holding Saturation Risk")
        st.plotly_chart(build_product_saturation_bar(filtered_df), use_container_width=True)
        
    c3, c4 = st.columns(2)
    with c3:
        st.subheader("Gender Variance Waterfall Bridge")
        st.plotly_chart(build_gender_disparity_waterfall(filtered_df), use_container_width=True)
    with c4:
        st.subheader("Member Engagement vs. Credit Card Matrix")
        st.plotly_chart(build_engagement_heatmap(filtered_df), use_container_width=True)

# TAB 4: HIGH-VALUE CAPITAL RISK EXPLORER
with tab4:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("4-Quadrant Balance vs. Salary Matrix")
        st.plotly_chart(build_high_value_quadrant_matrix(filtered_df), use_container_width=True)
    with c2:
        st.subheader("Funded vs. Zero-Balance Churn Breakdown")
        st.plotly_chart(build_zero_vs_funded_donut(filtered_df), use_container_width=True)
        
    c3, c4 = st.columns(2)
    with c3:
        st.subheader("Top Balance Decile Cumulative Capital Loss")
        st.plotly_chart(build_top_decile_loss_bar(filtered_df), use_container_width=True)
    with c4:
        st.subheader("High-Value Churn Rate by Tenure Group")
        st.plotly_chart(build_tenure_high_value_bar(filtered_df), use_container_width=True)

# TAB 5: WHAT-IF RETENTION ENGINE
with tab5:
    st.subheader("Executive Intervention Controls")
    s1, s2, s3 = st.columns(3)
    with s1:
        sim_german = st.slider("German Retention Campaign (% Churn Reduction)", 0.0, 50.0, 20.0, 5.0)
    with s2:
        sim_midage = st.slider("Age 46–60 Targeted Outreach (% Churn Reduction)", 0.0, 50.0, 25.0, 5.0)
    with s3:
        sim_cross = st.slider("1-Product to 2-Product Cross-Sell Migration (%)", 0.0, 50.0, 15.0, 5.0)
        
    sim_res = run_retention_simulation(filtered_df, sim_german, sim_midage, sim_cross)
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Capital Preservation Impact Bridge")
        st.plotly_chart(build_retention_waterfall(sim_res), use_container_width=True)
    with c2:
        st.subheader("Targeting Sensitivity Matrix")
        st.plotly_chart(build_retention_sensitivity_heatmap(filtered_df), use_container_width=True)
        
    c3, c4 = st.columns(2)
    with c3:
        st.subheader("Cross-Sell Migration Churn Trajectory")
        st.plotly_chart(build_product_migration_model(filtered_df), use_container_width=True)
    with c4:
        st.subheader("Simulated Portfolio Churn vs. Target")
        st.plotly_chart(build_regulatory_gauge(sim_res['sim_churn_rate'], kpis['churn_rate']), use_container_width=True)